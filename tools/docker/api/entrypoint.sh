#!/usr/bin/env sh

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn api.wsgi:application --bind=0.0.0.0:8000 --workers=4 --timeout=3600 --reload --access-logfile -
