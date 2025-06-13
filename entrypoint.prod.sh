#!/usr/bin/env bash

set -e 

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn"
python -m gunicorn \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        webapp.wsgi:application