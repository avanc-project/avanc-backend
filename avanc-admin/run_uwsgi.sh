#!/usr/bin/env bash

python3 manage.py migrate --noinput
python3 manage.py createsuperuser --no-input || true
python3 manage.py collectstatic --noinput

set -e

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini
