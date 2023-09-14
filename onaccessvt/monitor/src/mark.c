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

#define CHECK(X) ({int __val = (X); if(__val == -1){logToFile("ERROR (%s:%d) -- %s\n", __FILE__, __LINE__, strerror(errno));exit(EXIT_FAILURE);} }) 

static int monitored_dir_counter = 0;
static int fd;

static unsigned int fan_mask = 
(	
	FAN_CREATE |
	FAN_ONDIR
	);

int mark(int argc, char *argv[], int fanotify_fd, bool recursive){
	/*Call the needed function based on the recursive value*/
	fd = fanotify_fd;
	if(recursive)
		add_mark_recursive(argc, argv);
	else
		add_mark(argc, argv);
	return monitored_dir_counter;
}

static void add_mark(int argc, char *argv[]){
	/*Mark one or more directories based on argv so we can monitor thoose folders*/
	monitored_dir_counter = (argc - 1);
	char *input_path;
	char *marked_absolute_path;
	for(int c = 1; argv[c] != NULL; ++c){
		input_path = argv[c];
		marked_absolute_path = realpath(input_path, NULL);
		CHECK(fanotify_mark(fd, FAN_MARK_ADD, fan_mask, AT_FDCWD, input_path));
		logToFile(MSG_MONITORING_IN, marked_absolute_path);
	}
}

static void add_mark_recursive(int argc, char *argv[]){
	/*Mark directories in a recursive way using nftw to go through the path tree*/
	int nftw_result;
	char *input_path;

	for(int c = 2; argv[c] != NULL; ++c){
		input_path = argv[c];
		CHECK(nftw(input_path, add_entry, USE_FDS, FTW_PHYS));
	}
	
}

static int add_entry(const char *filepath, const struct stat *info, const int typeflag, struct FTW *pathinfo){
	/*This function is called for every entry found by the nftw function*/
	if(S_ISDIR(info->st_mode)){
		/*Check if the entry is a folder, print a message and mark it*/
		logToFile(MSG_MONITORING_IN, filepath); //Debug
		monitored_dir_counter++;
		CHECK(fanotify_mark(fd, FAN_MARK_ADD, fan_mask, AT_FDCWD, filepath));
	}
	return 0;
}