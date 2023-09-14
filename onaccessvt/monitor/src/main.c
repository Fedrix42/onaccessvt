#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/fanotify.h>
#include <sys/stat.h>
#include <limits.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <signal.h>
#include "main.h"
#include "mark.h"
#include "logger.h"
#include "usage.h"

#define CHECK(X) ({int __val = (X); if(__val == -1){logToFile("ERROR (%s:%d) -- %s\n", __FILE__, __LINE__, strerror(errno));exit(EXIT_FAILURE);} }) 

//Structures for file descriptor of fanotify notification group and stdin
static int fanotifty_fd;
static struct pollfd fds[2];

//Structures for data in fanotify fd
static struct fanotify_event_metadata buf[EVENTS_BUFFER]; 
static struct fanotify_event_metadata *metadata;
static struct fanotify_event_info_fid *info_fid;
static ssize_t lenght;

//Structure to hold event data
struct event_data e_data;

//File descriptor of file created used to get the directory where it was created 
static int fifo_fd;


static unsigned int fan_init_flags = 
(
	FAN_CLASS_NOTIF |
	FAN_CLOEXEC |
	FAN_NONBLOCK |
	FAN_REPORT_FID |
	FAN_REPORT_DFID_NAME
	); 



int main(int argc, char *argv[]){
	create_log_file();
	if(argc < 2){
		logToFile(ERR_MSG_USAGE, argv[0]);
       	exit(EXIT_FAILURE);
	}
	atexit(exit_routine);

	if(signal(SIGINT, sighandler) == SIG_ERR){
		logToFile("Error occurred while setting signal handler...\n");
		return EXIT_FAILURE;
	} else if (signal(SIGPIPE, sighandler) == SIG_ERR){
		logToFile("Error occurred while setting signal handler...\n");
		return EXIT_FAILURE;
	}

	
	logToFile("!This program should be run with super-user(root) permission!\n");
	fanotifty_fd = fan_initialize();
	logToFile("Initializing FIFO, waiting for reader to start...\n");
	fifo_fd = fifo_initialize();

	
	logToFile("Type 'q' key to terminate.\n");

	bool recursive_mode = false;
	recursive_mode = !strcmp(argv[1], "-r") ? true : false;

	logToFile("Recursive mode: %s \n", recursive_mode ? "ON" : "OFF");

	logToFile(MSG_ADD_OF_DIR, mark(argc, argv, fanotifty_fd, recursive_mode));

	monitor_events();

    exit(EXIT_SUCCESS);
}


int fifo_initialize(){
	/*Initialize the named pipe/fifo and check if there is any error*/
	int fd;
	if(mkfifo(FIFO_PATH, 0666) == -1){
		if(errno == EEXIST){
			if(remove(FIFO_PATH) == -1){
				perror("remove");
			}else {
				fifo_initialize();
			}
		}else {
			perror("mkfifo");
			exit(EXIT_FAILURE);
		}
	}
	CHECK(fd = open(FIFO_PATH, O_WRONLY));

	return fd;
}

int fan_initialize(){
	/*Inizialize fanotify notification group with specified arguments based.
	Check fanotify man page for more info...*/
	int fd = fanotify_init(fan_init_flags, O_RDONLY | O_LARGEFILE);
	CHECK(fd);
	fds[0].fd = STDIN_FILENO;        
	fds[0].events = POLLIN;          
	fds[1].fd = fd;     
	fds[1].events = POLLIN;
	return fd;
}


void monitor_events(){
	/*Check using poll() if there is any event available on the file descriptor for fanotify and STDIN*/
	int num_of_events;
	char input_from_user[2];
	nfds_t size_of_fds = 2;

	while(true){
		num_of_events = poll(fds, size_of_fds, -1); 

		if(num_of_events == -1){
			if (errno == EINTR)     
               continue;
           	perror("poll"); 
           	exit(EXIT_FAILURE);
		} else {
			if (fds[0].revents & POLLIN) {  //Check if there is a event for STDIN(The user can quit by sending q)
				if(read(STDIN_FILENO, &input_from_user, 2) > 0 && input_from_user[0] == 'q'){
					break;
				}

            }
            if (fds[1].revents & POLLIN) { //Check if there is any event available in the fanotify file descriptor
                handle_events();
            }
		}
	}
}

void handle_events(){
	/*Read from fanotify fd and handle every event found*/
	if(lenght = read(fanotifty_fd, buf, EVENTS_BUFFER)){
		if(lenght > 0){
			metadata = (struct fanotify_event_metadata*)buf;

			while(FAN_EVENT_OK(metadata, lenght)){ //-> Loop until there is no more event to handle 
				info_fid = (struct fanotify_event_info_fid*)(metadata+1);
				process_event(metadata);
				
				metadata = FAN_EVENT_NEXT(metadata, lenght); //-> Point to the next event
			}

		}
	}

}


void process_event(struct fanotify_event_metadata *metadata){	
	char symlink_proc[PATH_MAX];

	if(metadata->vers != FANOTIFY_METADATA_VERSION){
		logToFile(ERR_MSG_VERS_NOT_MATCH);
       	exit(EXIT_FAILURE);
	}

	//Get file handle which is useful for retrieving more informations
	struct file_handle *targeted_file_handle = (struct file_handle*)info_fid->handle;

	/*Debug
	logToFile("File handle struct:\nBytes: %d\nHandle type: %d\nFileID: %c\n", 
		targeted_file_handle->handle_bytes, targeted_file_handle->handle_type, targeted_file_handle->f_handle[0]);
	*/

	//Get the entry name which is then stored in a char array on the e_data struct
	char *temp_entry_name = targeted_file_handle->f_handle + targeted_file_handle->handle_bytes;
	for(int c = 0, lenght = strlen(temp_entry_name); c < lenght; ++c){
		e_data.entryname[c] = temp_entry_name[c];
	}

	//Get entry fd from file handle
	int targeted_entry_fd = open_by_handle_at(AT_FDCWD, targeted_file_handle, O_RDONLY);
	CHECK(targeted_entry_fd);

	//Retrieve directory name and store it in e_data struct
	snprintf(symlink_proc, sizeof(symlink_proc), "/proc/self/fd/%d", targeted_entry_fd);
	CHECK(readlink(symlink_proc, e_data.directory_path, sizeof(e_data.directory_path)));

	//Get pid and check if entry is a file
	e_data.pid = metadata->pid;
	struct stat entry_stat = get_entry_stat(targeted_entry_fd, temp_entry_name);
	e_data.inode = get_entry_inode(entry_stat);

	//Print and write data to fifo
	logToFile(MSG_EVENT_DATA, e_data.pid,e_data.directory_path, e_data.entryname,e_data.inode, is_entry_a_file(entry_stat) ? "Yes" : "No");
	CHECK(write(fifo_fd, &e_data, sizeof(e_data)));
	
	//Clear the buffers for the file path so they don't get concatenated
	memset(e_data.entryname, 0, sizeof(e_data.entryname));
	memset(e_data.directory_path, 0, sizeof(e_data.directory_path));

}


//Check if entry created is a file or directory
bool is_entry_a_file(struct stat entry_stat){
	if ((entry_stat.st_mode & S_IFMT) == S_IFREG){
		return true;
	}else {
		return false;
	}
}

int get_entry_inode(struct stat entry_stat){
	return entry_stat.st_ino;
}

struct stat get_entry_stat(int fd, char *entry_name){
	/*Get a stat struct hondling informations like inode and more about the entry(Useful for the functions above)*/
	struct stat entry_stat;
	if(fstatat(fd, entry_name, &entry_stat, 0) == -1){
		if (errno != ENOENT) {
           perror("fstatat");
           exit(EXIT_FAILURE);
       	}
       logToFile(ERR_MSG_ENTRY_NOT_EXISTS, entry_name);
       return entry_stat;
	}
	return entry_stat;
}

void exit_routine(){
	/*Function called every time exit() is called.
	This function remove the fifo from the file system and close log file and file descriptor*/
	char exit_message[] = "\nTerminating...\n";
	char remove_error_message[] = "Error while trying to remove fifo file!\n";
	if(remove(FIFO_PATH) == -1){
		logToFile(remove_error_message, sizeof(remove_error_message));
	}
	logToFile(exit_message, sizeof(exit_message));
	closeLogFile();
	close(fanotifty_fd);
	close(fifo_fd);
}

void sighandler(int signum){
	/*Function to handle signal like SIGTERM, SIGINT or SIGPIPE*/
	if(signum == SIGPIPE){
		char pipe_err[] = "\nSIGPIPE signal received, check if fifo reader is running...\n";
		logToFile(pipe_err, sizeof(pipe_err));
	}
	exit(EXIT_FAILURE);
}