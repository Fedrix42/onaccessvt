# Requirements check
## Linux kernel version
``` 
uname -r
```
Check that your kernel version is greater than 5.9
## Linux fanotify API enabled
``` 
cat /boot/config-<kernel_version>  | grep FANOTIFY
```
You should see the following:
```
CONFIG_FANOTIFY=y
CONFIG_FANOTIFY_ACCESS_PERMISSIONS=y
```
If you see ` CONFIG_FANOTIFY_ACCESS_PERMISSIONS is not set ` the software `will not work`.
## gcc
```
gcc --version
```
If you see `gcc: command not found ` you probably need to install gcc (Usually with apt).
## notify-send
```
notify-send --version
```
If you see `notify-send: command not found ` maybe notifications are not supported in your OS as they are in Ubuntu.
