#!/bin/bash

PRJ=`pwd | rev | cut -d "/" -f3 | rev`
gunicorn server.wsgi:application -w 5 --timeout 300 --limit-request-line 16382 --bind unix:/tmp/api.$PRJ.socket
cd .. && celery -A server worker --loglevel=warning
