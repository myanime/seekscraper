#!/usr/bin/env bash
echo "Poor Mans Cron"
echo "Starting in 1hrs"
sleep 3600
while true
do
    echo "Starting in 24hrs"
    sleep 86400
    gnome-terminal --command=/home/media/seek/local_seek.sh --display=:0
done

