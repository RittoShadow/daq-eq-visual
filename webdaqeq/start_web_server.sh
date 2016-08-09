#!/bin/bash
sleep 1
screen -AmdS server_shell bash
sleep 5
screen -S server_shell -p 0 -X stuff $'sudo python /home/pi/daq-eq-visual/webdaqeq/manage.py runserver 0.0.0.0:3000\r'
sleep 1
x-terminal-emulator -e "screen -x server_shell"

