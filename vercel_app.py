"""
Vercel deployment adapter for Django application
"""
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Add the current directory and parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
logging.info(f"Current directory: {current_dir}")
logging.info(f"Files in current directory: {os.listdir(current_dir)}")

# Ensure __init__.py files exist
for dir_name in ['AgricultureWholesale', 'agro', 'account']:
    init_path = os.path.join(current_dir, dir_name, '__init__.py')
    if os.path.isdir(os.path.join(current_dir, dir_name)) and not os.path.exists(init_path):
        try:
            with open(init_path, 'w') as f:
                pass
            logging.info(f"Created {init_path}")
        except Exception as e:
            logging.error(f"Failed to create {init_path}: {e}")

import django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# Manually define URL patterns instead of importing
from django.urls import include, path

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgricultureWholesale.settings')
django.setup()

# Define URL patterns directly
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agro.urls')),
    path('account/', include('account.urls')),
]

# Add static and media URL patterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Import WSGI app from Django
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# For Vercel
app = application 