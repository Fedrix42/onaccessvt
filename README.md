# OnAccess VirusTotal Scanner
OnAccess VirusTotal Scanner (OnAccessVT shortened) is a software, designed for linux, which scans files created in specified directories using VirusTotal engine.\
The tool does not yet supports file uploading so it makes a requests to VirusTotal API with the file HASH, retrieve the answer and display the result to the user.\
![Screenshot from 2023-09-14 18-09-11](https://github.com/Fedrix42/onaccessvt/assets/144663254/f668a7f8-8e0b-4b65-99b5-551cff1519b8)

Features:
* Automatic detection of browser downloads
* Recursive mode
* Multiple folders monitoring
* Notifications and event logging

**Software is currently tested and working on Ubuntu 22.04 and 23.04, not guaranteed it works on other environments**
## Check other solutions
This project is ispired by [ClamAV](https://www.clamav.net/) OnAccess scanning feature.\
I was searching for a security solution for my linux distro but I found ClamAV really slow when doing scanning(I mean, that's a real malware scan while here we are doing just a request to third-party service).\
**So if you want a real anti-virus/anti-malware go for ClamAV**, if you are looking for a less stable but lightweight solution then this may help you.

## Requirements
  * VirusTotal Account with a API-KEY, currently free with some limitations: [VT Public API limitations](https://developers.virustotal.com/reference/public-vs-premium-api)
  * Linux kernel version >= 5.9
  * Linux kernel fanotify API enabled
  * gcc (Usually pre-installed with OS, is a compiler for C language)
  * notify-send (Usually pre-installed with OS, is a tool used to send notifications to the user)
### Dependencies (Installed by setup.sh)
  * vt-py -> Is the official VirusTotal API library for Python3
  * python3-tk -> Is a GUI library for Python3

## [Requirements check](check_requirements.md)
## Installation
The software is made out of 2 main components: OnAccessVT Monitor and OnAccessVT Interface
Theese two components need to be executed with some arguments you must set on files **setup.sh** and **onaccessvt.start**

* Download the repository from github and unzip it(You can use curl, wget, git or use the download button)
```
git clone https://github.com/Fedrix42/onaccessvt.git
```
* Open the two files in the repo with a text editor and set the arguments according to the following usages in the variables `interface_args` in onaccessvt.start and `monitor_args` in setup.sh (Example below)

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

### > Example
My user in my OS is `frank`\
My api key is: `abc12345`\
I want to receive notifications even if a file has 0 malicious entries\
I want to recursively monitor folders: `/home/ubuntu/Desktop/f1` and `/home/ubuntu/Desktop/f2`
#### setup.sh
```
user='frank'
monitor_args='-r /home/ubuntu/Desktop/f1 /home/ubuntu/Desktop/f2'
...
```

#### onaccessvt.start
```
interface_args='-v abc12345'
...
```
On file **onaccessvt.start** you should also set DBUS environment variable according to the result of command:
```
env | grep DBUS_SESSION_BUS_ADDRESS  
```

### Final step of installation
```
cd onaccessvt && sudo ./setup.sh
```
Now you should be done. At reboot the software should start and you should see a notification of success come up.
If there is any error or you think something is not working(No notifications appear when file are created) then go to Troubleshooting section below.

## How to build
Interface component is written in python and it's executed by source code but if you want compile it you try with [Cython](https://cython.org/) (But probably will not work).\
To compile monitor component(which is written in C) you can use gcc:
```
gcc onaccessvt/monitor/src/main.c onaccessvt/monitor/src/mark.c onaccessvt/monitor/src/logger.c -o onaccessvt/monitor/bin/onaccessvt_monitor
```

## Troubleshooting
### Folders used by software
  * /opt/onaccessvt --> Contains source code and binaries executed at startup
  * /var/log/onaccessvt --> Contains log file with errors and detected events for interface and monitor components
  * /tmp/on_accessvt_fifo --> Named pipe/fifo created for IPC, deleted when monitor component shuts down
  * `crontab -e` --> Contains the crontab directives to start the monitor and the interface at boot

First thing you can check are the arguments. The folders you specify in the monitor argument should exists and the API key in the interface arguments should be valid(Check logs for this types of errors).\
Then you should check that crontab records was created correctly:
```
crontab -e
```
You should something like this(Comments could have been deleated):\
![image](https://github.com/Fedrix42/onaccessvt/assets/144663254/e52cda74-d446-4742-af85-9f183f949fb9)
```
sudo crontab -e
```
You should something like this(Comments could have been deleated):\
![image](https://github.com/Fedrix42/onaccessvt/assets/144663254/e01318b3-bd19-48bc-bf97-dcaf76ed9d62)

Check if you installed vt-py library:
```
pip list | grep vt-py
```
Check if you installed python3-tk library(Tkinter):
```
sudo apt list | grep python3-tk
```

## Disclaimer
I'm a student and I worked on this project alone, there a lot of of things which should be done better but it requires time and skill so suggestions and pull requests are really appreciated.

## To-Do
 - [ ] Better and easier installation process
 - [ ] Improve stability
 - [ ] File uploading
 - [ ] URL Scan
 - [ ] Better GUI and notifications
 - [ ] Implementation for other scanning platforms(Karspersky Threat Center, ...)




