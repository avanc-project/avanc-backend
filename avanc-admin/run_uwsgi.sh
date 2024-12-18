#!/usr/bin/env bash

python3 manage.py migrate --noinput
python3 manage.py createsuperuser --no-input || true
python3 manage.py collectstatic --noinput

set -e

chown -R www-data:www-data /opt/app/static /opt/app/media

uwsgi --strict --ini uwsgi.ini
