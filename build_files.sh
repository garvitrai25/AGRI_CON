#!/bin/bash
# Build script for Vercel deployment

echo "Current directory: $(pwd)"
echo "Listing files: $(ls -la)"

echo "Setting up minimal requirements.txt for Vercel deployment..."
cp requirements-minimal.txt requirements.txt

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Build completed!" 