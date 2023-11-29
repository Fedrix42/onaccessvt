#include <stdio.h>
#include <stdbool.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include "set_config.h"

static FILE *config_file_ptr;
bool recursive = false;
char *monitored_folders[MAX_FOLDERS_SUPPORTED];
int input_dir_counter = 0;

void set_config(){
    config_file_ptr = fopen(CONFIG_PATH, "r");
    clear_monitored_folders_pointers();
    read_content();
    fclose(config_file_ptr);
}

void read_content(){
    char *line = NULL;
    size_t len = 0;
    ssize_t nread;

    while((nread = getline(&line, &len, config_file_ptr)) != -1){
        //nread is the length of the string line(without null char)
        if(strstr(line, "#") != NULL){
            memset(line, 0x00, nread);
            continue;
        }
        if(strstr(line, "recursive") != NULL){
            if (strstr(line, "true") != NULL || strstr(line, "True") != NULL) {
                recursive = true;
            }
        } else {
            if(input_dir_counter >= MAX_FOLDERS_SUPPORTED)
                break;

            if (line[strlen(line) - 1] == '\n'){
                line[strlen(line)  - 1] = '\0';
            }

            monitored_folders[input_dir_counter] = malloc(sizeof(char)*(strlen(line) +1));
            str_copy(monitored_folders[input_dir_counter], line);
            monitored_folders[input_dir_counter][strlen(line)] = '\0';
            input_dir_counter++;
        }
    }
    free(line); //Memory is allocated by getline()
}

void free_monitored_folders(){
    for(int i = 0; i < input_dir_counter; ++i){
        free(monitored_folders[i]);
    }
    clear_monitored_folders_pointers();
}

void clear_monitored_folders_pointers(){
    for(int i = 0; i < MAX_FOLDERS_SUPPORTED; ++i){
        monitored_folders[i] = NULL;
    }
}

void str_copy(char *destination_string, char *source_string){
    for(int c = 0; source_string[c] != '\0'; ++c){
        destination_string[c] = source_string[c];
    }
}
