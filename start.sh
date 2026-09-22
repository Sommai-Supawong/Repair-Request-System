#!/usr/bin/env bash
set -e

echo "Initializing database..."
python -m flask --app app init-db

echo "Creating demo users..."
python -m flask --app app seed-demo

echo "Starting Gunicorn..."
exec gunicorn "app:create_app()" --bind 0.0.0.0:${PORT:-10000}