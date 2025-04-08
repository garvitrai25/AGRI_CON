#!/bin/bash
# Build script for Vercel deployment

# Echo some debug information
echo "Current directory: $(pwd)"
echo "Listing directory contents:"
ls -la

# Install setuptools first to provide distutils
echo "Installing setuptools..."
python3 -m pip install setuptools==57.0.0

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r requirements.txt

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

# Ensure proper permissions
chmod +x build_files.sh
echo "Set execution permissions for build script"

# Run migrations and collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Build completed successfully" 