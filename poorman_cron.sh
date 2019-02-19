#!/usr/bin/env bash
echo "Poor Mans Cron"
echo "Starting in 1hrs"
sleep 3600
while true
do
    echo "Starting in 24hrs"
    gnome-terminal --command=/home/myanime/seekscraper/local_seek.sh --display=:0
    sleep 86400
done

