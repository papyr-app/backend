#!/usr/bin/env bash
python manage.py db upgrade
gunicorn -k gevent -w 1 -b 0.0.0.0:8000 wsgi:app
