#!/usr/bin/env bash
export FLASK_APP=manage.py
flask db upgrade
gunicorn -k gevent -w 1 -b 0.0.0.0:8000 wsgi:app
