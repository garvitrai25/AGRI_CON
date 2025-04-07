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
touch AgricultureWholesale/__init__.py
touch agro/__init__.py
touch account/__init__.py
echo "Created __init__.py files for packages"

# Run migrations and collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --settings=custom_settings

echo "Build completed successfully" 