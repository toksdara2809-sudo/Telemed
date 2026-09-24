#!/bin/bash
# Vercel build script
echo "Building Django project..."
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_demo_data
echo "Build complete!"