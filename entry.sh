#!/bin/bash

printenv | grep -v "no_proxy" >> /home/code/.env

echo "Hello, entry.sh is running don't worry. Cron will start now."
sleep 10
cd /home/code && /usr/local/bin/python main.py

cron && tail -f /var/log/cron.log