#!/bin/bash
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Gunicorn processes
echo "Starting Gunicorn..."
exec gunicorn telemed_project.wsgi:application --bind 0.0.0.0:$PORT
