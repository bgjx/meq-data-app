#!/usr/bin/env bash
set -e 

# Ensure runtime directories exist and are writeable
mkdir -p /home/app/web/logs /home/app/web/staticfiles /home/app/web/media
chown -R appuser:appuser /home/app/web
chown -R appuser:appuser /home/app/web/staticfiles
chown -R appuser:appuser /home/app/web/media
chown -R appuser:appuser /home/app/web/logs

# Fix ownership of mounted volumes
echo 'Fixing volume permissions...'
chown -R appuser:appuser /home/app/web

# Switch to appuser and run the app
echo 'Switching to appuser and run the app...'
exec su -s /bin/bash/ appuser -c "
        echo 'Running database migrations...' &&
        python manage.py migrate --noinput &&

        echo 'Collecting static files...' &&
        python manage.py collectstatic --noinput &&

        echo 'Starting Gunicorn...' &&
        python -m gunicorn \
                --bind 0.0.0.0:${GUNICORN_PORT}\
                --workers ${GUNICORN_WORKERS} \
                --log-level info \
                --access-logfile - \
                --error-logfile - \
                webapp.wsgi:application
"

