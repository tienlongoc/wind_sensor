#!/bin/bash

source ~/.bashrc
source ./wind_sensor/bin/activate

day=$(date +"%Y%m%d")
hour=$(date +"%Y%m%d-%H")

python generate_charts.py --day="$day"
python generate_charts.py --hour="$hour"

if [ -f ./charts/daily/$day.html ] ; then
    cp ./charts/daily/$day.html ./charts/daily/current.html
else
    cp ./charts/daily/default.html ./charts/daily/current.html
fi
if [ -f ./charts/hourly/$hour.html ] ; then
    cp ./charts/hourly/$hour.html ./charts/hourly/current.html
else
    cp ./charts/hourly/default.html ./charts/hourly/current.html
fi
