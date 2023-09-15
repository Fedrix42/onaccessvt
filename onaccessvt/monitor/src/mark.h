#ifndef MARK_H
#define MARK_H
#define _GNU_SOURCE
#include <ftw.h>
#define USE_FDS 15

int mark(int fanotify_fd, bool recursive);
static void add_mark();
static void add_mark_recursive();
static int add_entry(const char *filepath, const struct stat *info, const int typeflag, struct FTW *pathinfo);


#endif