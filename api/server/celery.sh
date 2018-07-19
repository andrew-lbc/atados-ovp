#!/bin/bash
cd ..
celery multi stopwait worker1 --pidfile="/tmp/celery.%n.pid"
celery multi start worker1 -A server \
    --logfile="$HOME/api/logs/celery/%n%I.log" \
    --pidfile="/tmp/celery.%n.pid"