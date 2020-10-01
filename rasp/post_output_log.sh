#!/bin/bash

source ~/.bashrc

cd /home/pi/ws/wind_sensor/pyserial/logs/
for log in $(ls *txt); do
    if curl -d $log 35.246.96.248:5000; then
        mv $log $log.posted
    fi
done
