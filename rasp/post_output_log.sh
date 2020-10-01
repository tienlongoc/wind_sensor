#!/bin/bash

source ~/.bashrc
date
cd /home/pi/ws/wind_sensor/pyserial/logs/
for log in $(ls *txt); do
    curl --data-binary "@$log" 35.246.96.248:5100 -d "api-key=dev"
done
