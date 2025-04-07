import os
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent

def download_file(url, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {destination}")
    else:
        print(f"Failed to download: {url}")

# Define the files to download
files_to_download = {
    'glightbox/css/glightbox.min.css': 'https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/css/glightbox.min.css',
    'glightbox/js/glightbox.min.js': 'https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/js/glightbox.min.js',
    'isotope-layout/isotope.pkgd.min.js': 'https://cdn.jsdelivr.net/npm/isotope-layout@3.0.6/dist/isotope.pkgd.min.js',
}

def main():
    vendor_dir = BASE_DIR / 'staticfiles' / 'assets' / 'vendor'
    
    for file_path, url in files_to_download.items():
        destination = vendor_dir / file_path
        download_file(url, destination)

if __name__ == "__main__":
    main() 