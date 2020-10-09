#!/bin/bash

source ~/.bashrc
source ~/ws/wind_sensor/gcp/wind_sensor/bin/activate

day=$(date +"%Y%m%d")
hour=$(date +"%Y%m%d-%H")


python $HOME/ws/wind_sensor/gcp/generate_charts.py --day="$day" >> $HOME/ws/wind_sensor/gcp/log.txt
python $HOME/ws/wind_sensor/gcp/generate_charts.py --hour="$hour" >> $HOME/ws/wind_sensor/gcp/log.txt

if [ -f $HOME/ws/wind_sensor/gcp/charts/daily/$day.html ] ; then
    cp $HOME/ws/wind_sensor/gcp/charts/daily/$day.html $HOME/ws/wind_sensor/gcp/templates/current_day.html
else
    cp $HOME/ws/wind_sensor/gcp/charts/daily/default.html $HOME/ws/wind_sensor/gcp/templates/current_day.html
fi
if [ -f $HOME/ws/wind_sensor/gcp/charts/hourly/$hour.html ] ; then
    cp $HOME/ws/wind_sensor/gcp/charts/hourly/$hour.html $HOME/ws/wind_sensor/gcp/templates/current_hour.html
else
    cp $HOME/ws/wind_sensor/gcp/charts/hourly/default.html $HOME/ws/wind_sensor/gcp/templates/current_hour.html
fi
