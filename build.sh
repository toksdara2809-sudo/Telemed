#!/bin/bash
# Build script for deployment (Render, Vercel, etc.)
set -o errexit

echo "Building Django project..."
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
# Optional: seed data
# python manage.py seed_demo_data
echo "Build complete!"