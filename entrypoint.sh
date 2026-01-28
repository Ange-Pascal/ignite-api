#!/bin/sh
set -e

: "${PORT:=8080}"

echo "PORT=${PORT}"
echo "Waiting for database..."
python manage.py wait_for_db

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Applying migrations..."
  python manage.py migrate --noinput
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn app.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  --graceful-timeout 30 \
  --keep-alive 5 \
  --access-logfile - \
  --error-logfile -
