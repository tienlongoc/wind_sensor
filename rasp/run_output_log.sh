#!/bin/bash

source ~/.bashrc

# Set up crontab
if ! crontab -l | grep -q run_output_log.sh; then
    crontab -l > curr_cron
    echo '0 0 * * 0 /home/pi/ws/wind_sensor/rasp/run_output_log.sh >> /home/pi/ws/wind_sensor/rasp/log.txt' >> curr_cron
    crontab curr_cron
    rm curr_cron
fi
if ! crontab -l | grep -q post_output_log.sh; then
    crontab -l > curr_cron
    echo '0 * * * * /home/pi/ws/wind_sensor/rasp/post_output_log.sh >> /home/pi/ws/wind_sensor/rasp/log.txt' >> curr_cron
    crontab curr_cron
    rm curr_cron
fi

# Kill existing output_log.py process
echo "Killing existing output log process"
ps -ef | grep output_log.py | awk '{print $2}' | xargs kill -9
sleep 5

echo "Start new output log proces"
# Start new output_log.py process
nohup python3 /home/pi/ws/wind_sensor/pyserial/output_log.py >> log.txt 2>&1 &
