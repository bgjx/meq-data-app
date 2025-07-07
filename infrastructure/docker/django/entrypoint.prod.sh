#!/usr/bin/env bash
set -e 

# Ensure runtime directories exist and are writeable
mkdir -p /home/app/web/logs /home/app/web/staticfiles /home/app/web/media
chown -R appuser:appuser /home/app/web

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn"
exec python -m gunicorn \
        --bind 0.0.0.0:${GUNICORN_PORT}\
        --workers ${GUNICORN_WORKERS} \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        webapp.wsgi:application