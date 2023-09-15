#!/bin/bash
user='ubuntu'

#---Dependencies
sudo -u $user pip install vt-py
sudo apt install python3-tk
#---Dependencies

#Compile monitor
mkdir ./monitor/bin/
gcc ./monitor/src/main.c ./monitor/src/mark.c ./monitor/src/logger.c -o ./monitor/bin/onaccessvt_monitor
chmod +x ./monitor/bin/onaccessvt_monitor

#Copy current folder into /opt
sudo cp -r ../onaccessvt /opt/
sudo chown -R $user:$user /opt/onaccessvt/

#Create folder for logging
sudo mkdir /var/log/onaccessvt 
sudo mkdir /var/log/onaccessvt/interface
sudo mkdir /var/log/onaccessvt/monitor
sudo chown -R $user:$user /var/log/onaccessvt/

#Adding crontab for onaccessvt interface to user
sudo -u $user crontab -l > mycron
echo "@reboot /opt/onaccessvt/onaccessvt_interface.start" >> mycron
sudo -u $user crontab mycron
rm mycron

#Adding crontab for onaccessvt monitor to root user
crontab -l > mycron_root
echo "@reboot sleep 30s && /opt/onaccessvt/monitor/bin/onaccessvt_monitor $(echo $monitor_args)" >> #mycron_root
crontab mycron_root
rm mycron_root
