#!/bin/bash
# Build script for Vercel deployment

echo "Setting up minimal requirements.txt for Vercel deployment..."
cp requirements-minimal.txt requirements.txt

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed!" 