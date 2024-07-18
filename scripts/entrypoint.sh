#!/usr/bin/env bash
#
./scripts/wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is up"

export FLASK_APP=manage.py
flask db upgrade

if [ "$1" == "dev" ]; then
  python run.py
else
  gunicorn -k gevent -w 1 -b 0.0.0.0:8000 wsgi:app
fi
