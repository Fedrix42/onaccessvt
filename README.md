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
### 1. Download the repository from github and unzip it(You can use curl, wget, git or use the download button)
```
git clone https://github.com/Fedrix42/onaccessvt.git
```
### 2. Open file onaccessvt_interface.start(inside onaccessvt dir) and set the environment variable according to the comment.
```
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
#This environment variable should be set according to the value you find doing: env | grep DBUS_SESSION_BUS_ADDRESS  
#Default value should work in most of the cases I guess
```
### 3. Open setup.sh and change the variable 'user' with your OS user
You can check your username in terminal by typing:
```
whoami
```

### 4. Configurations
* Set the folders you want to monitor in file onaccessvt/monitor/monitor.config according to comments.
* Set your api-key and the verbosity in file onaccessvt/interface/interface.config according to comments.
### 5. Final step
**Be sure you are into the folder containing setup.sh**
```
chmod +x setup.sh && sudo ./setup.sh
```
Now you should be done. At reboot the software should start and you should see a notification of success come up.
If there is any error or you think something is not working(No notifications appear when file are created) then go to Troubleshooting section below.

## How to build
Interface component is written in python and it's executed by source code but if you want compile it try with [Cython](https://cython.org/) (But probably will not work).\
To compile monitor component(which is written in C) you can use gcc:
```
gcc onaccessvt/monitor/src/main.c onaccessvt/monitor/src/mark.c onaccessvt/monitor/src/logger.c onaccessvt/monitor/src/set_config.c -o onaccessvt/monitor/bin/onaccessvt_monitor
```

## Troubleshooting
### Folders used by software
  * /opt/onaccessvt --> Contains source code and binaries executed at startup
  * /var/log/onaccessvt --> Contains log file with errors and detected events for interface and monitor components
  * /tmp/on_accessvt_fifo --> Named pipe/fifo created for IPC, deleted when monitor component shuts down
  * `crontab -e` --> Contains the crontab directives to start the monitor and the interface at boot

First thing you can check are the configurations. The folders you specify in the monitor config should exists and the API key in the interface config should be valid(Check logs for this types of errors).\
Then you should check that crontab records was created correctly:
```
crontab -e
```
You should something like this(Comments could have been deleted):\
![image](https://github.com/Fedrix42/onaccessvt/assets/144663254/e52cda74-d446-4742-af85-9f183f949fb9)
```
sudo crontab -e
```
You should something like this(Comments could have been deleted):\
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
 - [x] Better and easier installation/configuration process
 - [ ] Improve stability
 - [ ] File uploading
 - [ ] URL Scan
 - [ ] Better GUI and notifications
 - [ ] Implementation for other scanning platforms(Karspersky Threat Center, ...)




