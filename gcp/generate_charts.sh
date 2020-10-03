#!/bin/bash

source ~/.bashrc
source ~/ws/wind_sensor/gcp/wind_sensor/bin/activate

day=$(date +"%Y%m%d")
hour=$(date +"%Y%m%d-%H")

python generate_charts.py --day="$day"
python generate_charts.py --hour="$hour"

if [ -f ./charts/daily/$day.html ] ; then
    cp ./charts/daily/$day.html ./templates/current_day.html
else
    cp ./charts/daily/default.html ./templates/current_day.html
fi
if [ -f ./charts/hourly/$hour.html ] ; then
    cp ./charts/hourly/$hour.html ./templates/current_hour.html
else
    cp ./charts/hourly/default.html ./templates/current_hour.html
fi
