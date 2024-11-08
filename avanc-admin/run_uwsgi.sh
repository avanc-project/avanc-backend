#!/usr/bin/env bash

python3 manage.py migrate --noinput --fake
python3 manage.py createsuperuser --no-input || true
python3 manage.py collectstatic --noinput

python manage.py compilemessages -l en

set -e

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini
