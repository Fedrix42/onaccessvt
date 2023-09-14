#ifndef USAGE
#define USAGE

#define ERR_MSG_USAGE "!This program should be run with super-user(root) permission!\n\
Usage: %s [-r] [FOLDER...] \n\
You can specify more folders separed by spaces\n\
Options: \n\
-r, recursive mode: monitor every specified folder recursively(Use with caution, may impact performance)\n"

#define ERR_MSG_ENTRY_NOT_EXISTS "\tError - Entry '%s' does not exist anymore.\n"
#define ERR_MSG_VERS_NOT_MATCH "An error was encountered while processing an event.\nEvent metadata version(run time) doesn't match the version at compile time.\n"

#define MSG_MONITORING_IN "Monitoring FAN_CREATE events in: %s\n"
#define MSG_ADD_OF_DIR "Going to monitor a total of %d directories.\n"


#define MSG_EVENT_DATA "\n\
--Start of event data--\n\
PID: %d \n\
Directory path: %s \n\
Entry name: %s \n\
Inode: %d \n\
Is entry a file: %s \n\
--End of event data--\n\
"

#endif
