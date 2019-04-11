#!/bin/bash

PRJ=`pwd | rev | cut -d "/" -f3 | rev`
celery multi stopwait worker1 --pidfile="/tmp/celery.%n.pid"
celery multi start worker1 -A server \
    --logfile="$HOME/api/logs/celery/%n%I.log" \
    --pidfile="/tmp/celery.%n.pid"
gunicorn server.wsgi:application -w 5 --timeout 300 --limit-request-line 16382 --bind unix:/tmp/api.$PRJ.socket