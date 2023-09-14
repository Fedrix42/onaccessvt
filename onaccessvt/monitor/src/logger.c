#include <stdio.h>
#include <time.h>
#include <errno.h>
#include <limits.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include "logger.h"

static FILE *logger_file_ptr;

void logToFile(const char* format, ...){
	/*Log some formatted string to the logfile and print it*/
	char buffer[512];
	va_list args;

	va_start(args, format);
	vsnprintf(buffer, sizeof(buffer), format, args);

	fprintf(logger_file_ptr,"%s",buffer);
	printf("%s", buffer);

	va_end(args);
}

void create_log_file(){
	/*Create a log file based on current datetime*/
	time_t t = time(NULL);
  	struct tm tm = *localtime(&t);
  	char *log_filename = (char*)malloc(PATH_MAX * sizeof(char));
	sprintf(log_filename, "/var/log/onaccessvt/monitor/log - %d-%02d-%02d %02d:%02d:%02d", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
	logger_file_ptr = fopen(log_filename, "w");
	if(logger_file_ptr == 0){
		printf("ERROR (%s:%d) -- %s\n, ",__FILE__, __LINE__, strerror(errno));
		exit(EXIT_FAILURE);
	}
}

void closeLogFile(){
	fclose(logger_file_ptr);
}