#ifndef MAIN_H
#define MAIN_H

#define EVENTS_BUFFER 8192
#define FIFO_PATH "/tmp/on_accessvt_fifo"


struct event_data {
	int pid; //4 bytes
	char directory_path[PATH_MAX]; //4096 bytes
	char entryname[PATH_MAX]; //4096 bytes
	int inode; //4 bytes
};


int fan_initialize();
int fifo_initialize();
void monitor_events();
void handle_events();
void process_event(struct fanotify_event_metadata *metadata);
bool is_entry_a_file(struct stat entry_stat);
struct stat get_entry_stat(int fd, char *entry_name);
int get_entry_inode(struct stat entry_stat);
void exit_routine();
void sighandler(int signum);

#endif