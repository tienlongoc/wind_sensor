#!/bin/bash

source ~/.bashrc

source ~/ws/wind_sensor/gcp/wind_sensor/bin/activate

ps -ef | grep flask_api.py | awk '{print $2}' | xargs kill -9
echo Starting flask_api.py
nohup python $HOME/ws/wind_sensor/gcp/flask_api.py >> log.txt 2>&1 &

