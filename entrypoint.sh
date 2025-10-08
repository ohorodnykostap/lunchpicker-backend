#!/bin/sh

echo "Running migrations..."
python3 manage.py migrate

echo "Starting server..."
exec python3 manage.py runserver 0.0.0.0:8000

