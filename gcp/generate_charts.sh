#!/bin/bash

source ~/.bashrc

day=$(date +"%Y%m%d")
hour=$(date +"%Y%m%d-%H")

python generate_charts.py --day="$day"
python generate_charts.py --hour="$hour"

