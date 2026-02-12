#!/bin/sh
set -e

# On définit le port par défaut
: "${PORT:=8080}"

echo "Waiting for database..."
python manage.py wait_for_db || true

echo "Applying migrations..."
python manage.py migrate --noinput || true


echo "--- SEEDING START ---"
python manage.py seed_users || echo "Seed users failed"
python manage.py seed_categories || echo "Seed categories failed"
echo "--- SEEDING END ---"

echo "Collecting static files..."
python manage.py collectstatic --noinput || true


# SI aucune commande n'est passée au conteneur, on lance Gunicorn (PROD)
# SINON on exécute la commande passée (LOCAL / DEBUG)
if [ -z "$1" ]; then
    echo "Starting Gunicorn (Production mode)..."
    exec gunicorn app.wsgi:application \
      --bind 0.0.0.0:${PORT} \
      --workers 2 \
      --threads 4 \
      --timeout 0
else
    echo "Starting Command (Development mode): $@"
    exec "$@"
fi
