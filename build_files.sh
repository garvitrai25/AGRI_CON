#!/bin/bash
# Build script for Vercel deployment

# Echo some debug information
echo "Current directory: $(pwd)"
echo "Listing directory contents:"
ls -la

# Create a debug directory list
find . -type d | sort > directory_structure.txt
echo "Created directory structure file"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r requirements-minimal.txt

# Create necessary directories
mkdir -p staticfiles
echo "Created staticfiles directory"

# Create __init__.py files to make sure Python recognizes the directories as packages
mkdir -p AgricultureWholesale
mkdir -p agro
mkdir -p account
touch AgricultureWholesale/__init__.py
touch agro/__init__.py
touch account/__init__.py
echo "Created __init__.py files for packages"

# Ensure the vercel_app.py has execution permissions
chmod +x vercel_app.py
echo "Set execution permissions for vercel_app.py"

# Run migrations and collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Build completed successfully" 