#!/bin/bash

source ~/.bashrc
date
cd /home/pi/ws/wind_sensor/pyserial/logs/
for log in $(ls *txt); do
    rm tmp
    curl --data-binary "@$log" 35.246.96.248:5100 -d "api-key=dev" > tmp 2>&1
    if grep "post request received successfully" tmp; then
        echo "post success"
        mv $log $log.posted$(date +"%H%M%S")
	rm tmp
    else
        echo "post fail"
    fi
done
