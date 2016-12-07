#!/bin/sh
# launcher.sh
# navigate to base directory and execute python main script
clear > /dev/tty1
cd /
cd home/pi/lumos
# sudo python main.py
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service
sudo python main.py
