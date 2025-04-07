#!/bin/bash
# Build script for Vercel deployment

echo "Setting up requirements.txt for Vercel deployment..."
cp requirements-vercel.txt requirements.txt

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed!" 