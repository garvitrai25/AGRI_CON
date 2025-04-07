import importlib.util
import logging
import os
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

logging.info("Starting index.py...")

# Add the project directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
logging.info(f"Added {BASE_DIR} to sys.path")

# Patch for missing distutils in Vercel environment
# This needs to be done before importing Django
logging.info("Patching for missing distutils...")

class LooseVersion:
    def __init__(self, version_string):
        self.version_string = version_string
    def __str__(self):
        return self.version_string
    def __repr__(self):
        return self.version_string
    def __eq__(self, other):
        return str(self) == str(other)
    def __lt__(self, other):
        return str(self) < str(other)
    def __gt__(self, other):
        return str(self) > str(other)

# Create a fake distutils.version module
class FakeDistutilsVersion:
    LooseVersion = LooseVersion

# Create a fake distutils module
class FakeDistutils:
    version = FakeDistutilsVersion

# Add it to sys.modules
sys.modules['distutils'] = FakeDistutils
sys.modules['distutils.version'] = FakeDistutilsVersion
logging.info("Successfully patched distutils.version.LooseVersion")

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgricultureWholesale.settings')
logging.info("Using AgricultureWholesale.settings")

try:
    # Debug environment
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current directory contents: {os.listdir(BASE_DIR)}")
    
    # Initialize WSGI application
    logging.info("Importing Django WSGI application...")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.info("WSGI application initialized successfully")
except Exception as e:
    logging.error(f"Error initializing application: {e}", exc_info=True)
    
    # Create a fallback application that returns error details
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        
        error_message = f"""
        <html>
        <head><title>Error in Vercel Deployment</title></head>
        <body>
            <h1>Error in Vercel Deployment</h1>
            <p>There was an error initializing the Django application:</p>
            <pre>{str(e)}</pre>
            <h2>Environment Information:</h2>
            <ul>
                <li>Python Version: {sys.version}</li>
                <li>Working Directory: {os.getcwd()}</li>
                <li>Contents: {', '.join(os.listdir('.'))}</li>
                <li>sys.path: {sys.path}</li>
            </ul>
        </body>
        </html>
        """
        return [error_message.encode()]

# Handler for Vercel serverless function
app = application 