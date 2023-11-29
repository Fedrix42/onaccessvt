#ifndef CONFIG
#define CONFIG
#define CONFIG_PATH "/opt/onaccessvt/monitor/monitor.config"
#define MAX_FOLDERS_SUPPORTED 16
#include <limits.h>

extern bool recursive;
extern char *monitored_folders[MAX_FOLDERS_SUPPORTED];
extern int input_dir_counter;

void set_config();
void read_content();
void free_monitored_folders();
static void str_copy(char *destination_string, char *source_string);

#endif