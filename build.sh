#!/usr/bin/env bash
# Render / Railway start script
set -o errexit
python manage.py migrate --noinput
python manage.py seed_demo
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
