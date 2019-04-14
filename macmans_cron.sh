#!/usr/bin/env bash
echo "Poor Mans Cron"
sleep 5
echo "Starting"
osascript -e 'tell application "Terminal" to do script "/Users/ryan/repos/seekscraper/local_seek.sh"'

while true
do
    echo "Starting in 24hrs"
    sleep 86400
    osascript -e 'tell application "Terminal" to do script "/Users/ryan/repos/seekscraper/local_seek.sh"'
done