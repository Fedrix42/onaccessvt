#define _GNU_SOURCE
#include <sys/fanotify.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "mark.h"
#include "usage.h"
#include "logger.h"
#include "set_config.h"

#define CHECK(X) ({int __val = (X); if(__val == -1){logToFile("ERROR (%s:%d) -- %s\n", __FILE__, __LINE__, strerror(errno));exit(EXIT_FAILURE);} }) 

static int monitored_dir_counter = 0;
static int fd;

static unsigned int fan_mask = 
(	
	FAN_CREATE |
	FAN_ONDIR
	);

int mark(int fanotify_fd, bool recursive){
	/*Call the needed function based on the recursive value*/
	fd = fanotify_fd;
	if(recursive)
		add_mark_recursive();
	else
		add_mark();
	free_monitored_folders();
	return monitored_dir_counter;
}

static void add_mark(){
	/*Mark one or more directories based on monitored_folders got by config file so we can monitor thoose monitored_folders*/
	monitored_dir_counter = input_dir_counter;
	char *folder_path;
	for(int i = 0; i < input_dir_counter; i++){
		folder_path = monitored_folders[i];
		mark_with_checks(folder_path);
	}
}

static void add_mark_recursive(){
	/*Mark directories in a recursive way using nftw to go through the path tree*/
	int nftw_result;
	char *folder_path;

	for(int i = 0; i < input_dir_counter; i++){
		folder_path = monitored_folders[i];
		CHECK(nftw(folder_path, add_entry, USE_FDS, FTW_PHYS));
	}
	
}

static int add_entry(const char *filepath, const struct stat *info, const int typeflag, struct FTW *pathinfo){
	/*This function is called for every entry found by the nftw function*/
	if(S_ISDIR(info->st_mode)){
		/*Check if the entry is a folder and mark it*/
		mark_with_checks(filepath); //FilePath corresponds to FolderPath
		monitored_dir_counter++;
	}
	return 0;
}

static void mark_with_checks(const char* folder_path){
	int mark_returned = fanotify_mark(fd, FAN_MARK_ADD, fan_mask, AT_FDCWD, folder_path);
	if(mark_returned == -1){
		if(errno == ENOENT){
			logToFile("ERROR (__mark_with_checks__()) -- Directory %s does not exists!", folder_path);
		} else {
			logToFile("ERROR (__mark_with_checks__()) -- %s", strerror(errno));
		}
		exit(EXIT_FAILURE);
	}else {
		logToFile(MSG_MONITORING_IN, folder_path);
	}
}
