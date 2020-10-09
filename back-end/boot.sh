#!/usr/bin/env bash

source venv/bin/activate
while true; do
    flask db upgrade
    flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - madblog:app #change