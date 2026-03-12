#!/bin/sh

printenv > /etc/environment

echo "$CRON_SCHEDULE /usr/local/bin/python /app/replicate.py >> $LOG_FILE 2>&1" | crontab -

cron

tail -f $LOG_FILE