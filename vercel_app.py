import importlib.util
import logging
import os
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Add the project directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
logging.info(f"Added {BASE_DIR} to sys.path")

# Create necessary directories and __init__.py files
dirs = ['AgricultureWholesale', 'agro', 'account']
for dir_name in dirs:
    os.makedirs(os.path.join(BASE_DIR, dir_name), exist_ok=True)
    init_path = os.path.join(BASE_DIR, dir_name, '__init__.py')
    if not os.path.exists(init_path):
        try:
            open(init_path, 'a').close()
            logging.info(f"Created {init_path}")
        except Exception as e:
            logging.warning(f"Could not create {init_path}: {e}")

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgricultureWholesale.settings')
logging.info("Using AgricultureWholesale.settings")

# Patch for missing distutils in Vercel environment
# This needs to be done before importing Django
if importlib.util.find_spec("distutils") is None:
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

try:
    # Debug environment
    logging.info(f"Environment variables: {[f'{k}={v}' for k, v in os.environ.items() if not k.startswith('AWS_')]}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current directory contents: {os.listdir(BASE_DIR)}")
    
    # Initialize WSGI application
    logging.info("Attempting to import Django WSGI application...")
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