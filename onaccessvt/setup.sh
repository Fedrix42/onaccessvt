#!/bin/bash
user='fedrix'

#Check if script is runned with sudo
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

#---Dependencies
sudo -u $user pip install vt-py
sudo apt install python3-tk
#---Dependencies

#Compile monitor
mkdir ./monitor/bin/
gcc ./monitor/src/main.c ./monitor/src/mark.c ./monitor/src/logger.c ./monitor/src/set_config.c -o ./monitor/bin/onaccessvt_monitor
chmod +x ./monitor/bin/onaccessvt_monitor

#Copy current folder into /opt
sudo cp -r ../onaccessvt /opt/
sudo chown -R $user:$user /opt/onaccessvt/

#Create folder for logging
sudo mkdir /var/log/onaccessvt 
sudo mkdir /var/log/onaccessvt/interface
sudo mkdir /var/log/onaccessvt/monitor
sudo chown -R $user:$user /var/log/onaccessvt/

#Adding crontab for onaccessvt interface to user(only if it was not added before)
sudo -u $user crontab -l > mycron
if ! [[ $(cat mycron | grep onaccessvt_interface) ]]; then
	echo "@reboot /opt/onaccessvt/onaccessvt_interface.start" >> mycron
	sudo -u $user crontab mycron
fi
rm mycron


#Adding crontab for onaccessvt monitor to root user(only if it was not added before)
crontab -l > mycron_root
if ! [[ $(cat mycron_root | grep onaccessvt_monitor) ]]; then
	echo "@reboot sleep 30s && /opt/onaccessvt/monitor/bin/onaccessvt_monitor $(echo $monitor_args)" >> mycron_root
	crontab mycron_root
fi
rm mycron_root
