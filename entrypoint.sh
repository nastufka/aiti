#!/bin/sh

echo "⏳ Waiting for database..."

while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Database is ready"
cd app
ls -l
python manage.py migrate

echo "🚀 Starting server"
python manage.py runserver 0.0.0.0:8000