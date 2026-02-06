#!/bin/sh
set -e

: "${PORT:=8080}"

echo "PORT=${PORT}"

echo "Applying migrations..."
python manage.py migrate --noinput || true

# 🔥 AJOUT ICI : Création des utilisateurs par défaut
echo "Seeding default users..."
python manage.py seed_users || echo "Seed users failed or already exists"

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting Gunicorn..."
exec gunicorn app.wsgi:application \
  --bind 0.0.0.0:${PORT} \
  --workers 2 \
  --threads 4 \
  --timeout 0 \
  --access-logfile - \
  --error-logfile -

