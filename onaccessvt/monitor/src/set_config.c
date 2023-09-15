#include <stdio.h>
#include <stdbool.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include "set_config.h"

static FILE *config_file_ptr;
bool recursive = false;
char monitored_folders[PATH_MAX][MAX_FOLDERS_SUPPORTED];
int input_dir_counter = 0;

void set_config(){
    config_file_ptr = fopen(CONFIG_PATH, "r");
    read_content();
    fclose(config_file_ptr);
}

void read_content(){
    char line[PATH_MAX];

    while(fgets(line, sizeof(line), config_file_ptr)){
        //printf("%s\n", line);
        if(strstr(line, "#") != NULL){
            continue;
        }
        if(strstr(line, "recursive") != NULL){
            if (strstr(line, "true") != NULL || strstr(line, "True") != NULL) {
                recursive = true;
            }
        } else {
            //printf("Size of line: %ld\n", strlen(line));
            if (line[strlen(line) - 1] == '\n')
                line[strlen(line) - 1] = '\0';
            strcpy(monitored_folders[input_dir_counter], line);
            input_dir_counter++;
        }
        memset(line, 0x00, sizeof(line));
    }
}