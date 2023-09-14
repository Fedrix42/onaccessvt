# OnAccess VirusTotal Scanner
OnAccess VirusTotal Scanner (OnAccessVT shortened) is a software, designed for linux, that scans files created in specified directories using VirusTotal engine.
The tool does not yet supports file uploading so it makes a requests to VirusTotal API with the file HASH and retrieve the answer displaying it to the user.

**Software is currently tested and working on Ubuntu 22.04 and 23.04, not guaranteed it works on other environments**

## Requirements
  * VirusTotal Account with a API-KEY, currently free with some limitations: [VT Public API limitations](https://developers.virustotal.com/reference/public-vs-premium-api)
  * Linux kernel version >= 5.9
  * Linux kernel fanotify API enabled
  * Root permissions for installation
  * Crontab for user and root
  * vt-py (Installed during setup, is the official VirusTotal API library for Python3)
  * python3-tk (Installed during setup, is a GUI library for Python3)
  * gcc (Usually pre-installed with OS, is a compiler for C language)
  * notify-send (Usually pre-installed with OS, is a tool used to send notifications to the user)

## Requirements check
### Linux kernel version
``` 
uname -r
```
### Linux fanotify API enabled
``` 
cat /boot/config-<kernel_version>  | grep FANOTIFY
```
You should see the following:
```
CONFIG_FANOTIFY=y
CONFIG_FANOTIFY_ACCESS_PERMISSIONS=y
```
If you see ` CONFIG_FANOTIFY_ACCESS_PERMISSIONS is not set ` the software `will not work`.
### gcc
```
gcc --version
```
If you see `gcc: command not found ` you probably need to install gcc (Usually with apt).
### notify-send
```
notify-send --version
```
If you see `notify-send: command not found ` probably notifications are not supported in your OS.
## Installation
The software is made out of 2 main components: OnAccessVT Monitor and OnAccessVT Interface\
Theese two components need to be executed with some arguments you must set on files setup.sh and onaccessvt.start\
Open the two files with a text editor and set the arguments according to the following usages in the variables `interface_args` in onaccessvt.start and `monitor_args` in setup.sh

### Usage of monitor
```
$ ./onaccessvt_monitor
!This program should be run with super-user(root) permission!
Usage: ./monitor/bin/onaccessvt_monitor [-r] [FOLDER...]
You can specify more folders separed by spaces
Options: 
-r, recursive mode: monitor every specified folder recursively(Use with caution, may impact performance)
```
### Usage of interface
```
$ python3 main.py --help
usage: main.py [-h] [-v] [--nt NT] api-key
positional arguments:
  api-key        The API key from virus total website(account required)
options:
  -h, --help     show this help message and exit
  -v, --verbose  If set show a notification for every event detected even if they have 0 malicious entries
  --nt NT        The timeout, expressed in SECONDS, for notifications - DEFAULT is 5
```



