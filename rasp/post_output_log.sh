#!/bin/bash

source ~/.bashrc

cd /home/pi/ws/wind_sensor/pyserial/logs/
for log in $(ls *txt); do
    if -d "api-key=dev" curl --data-binary "@$log" 35.246.96.248:5100; then
        mv $log $log.posted
    fi
done
