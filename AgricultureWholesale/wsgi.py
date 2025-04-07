import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgricultureWholesale.settings')

application = get_wsgi_application()

# Handler for Vercel serverless function
app = application 