import logging
import os
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Add the project directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
logging.info(f"Added {BASE_DIR} to sys.path")

# Create necessary __init__.py files if they don't exist
init_paths = [
    os.path.join(BASE_DIR, 'AgricultureWholesale', '__init__.py'),
    os.path.join(BASE_DIR, 'agro', '__init__.py'),
    os.path.join(BASE_DIR, 'account', '__init__.py'),
]
for init_path in init_paths:
    if not os.path.exists(init_path):
        try:
            open(init_path, 'a').close()
            logging.info(f"Created {init_path}")
        except Exception as e:
            logging.warning(f"Could not create {init_path}: {e}")

# Always use the standard settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgricultureWholesale.settings')
logging.info("Using standard settings")

try:
    # Initialize WSGI application
    from django.core.wsgi import get_wsgi_application
    logging.info("Starting WSGI application...")
    logging.info(f"sys.path: {sys.path}")
    logging.info(f"Current directory: {os.getcwd()}")
    logging.info(f"Files in current directory: {os.listdir('.')}")
    
    try:
        logging.info(f"Files in AgricultureWholesale: {os.listdir('AgricultureWholesale')}")
    except Exception as e:
        logging.error(f"Could not list files in AgricultureWholesale: {e}")
    
    # Import the urls module explicitly to test if it can be found
    try:
        import AgricultureWholesale.urls
        logging.info("Successfully imported AgricultureWholesale.urls")
    except ImportError as e:
        logging.error(f"Failed to import AgricultureWholesale.urls: {e}")
        
    application = get_wsgi_application()
    logging.info("WSGI application initialized successfully")
except Exception as e:
    logging.error(f"Error initializing WSGI application: {e}", exc_info=True)
    raise

# Handler for Vercel serverless function
app = application 