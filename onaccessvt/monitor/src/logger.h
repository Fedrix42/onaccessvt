#ifndef LOGGER
#define LOGGER

void logToFile(const char* format, ...);
void create_log_file();
void closeLogFile();

#endif