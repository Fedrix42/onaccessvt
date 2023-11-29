#ifndef MARK_H
#define MARK_H
#define _GNU_SOURCE
#include <ftw.h>
#define USE_FDS 15

int mark(int fanotify_fd, bool recursive);
void add_mark();
void add_mark_recursive();
int add_entry(const char *filepath, const struct stat *info, const int typeflag, struct FTW *pathinfo);
void mark_with_checks(const char* folder_path);


#endif