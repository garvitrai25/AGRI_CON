import json
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('vercel_app')

# Add current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def debug_info():
    """Collect debug information about the environment"""
    info = {
        'current_dir': current_dir,
        'sys_path': sys.path,
        'python_version': sys.version,
        'dir_contents': os.listdir(current_dir),
        'env_vars': {k: v for k, v in os.environ.items() if not k.startswith('AWS_')},
    }
    
    # Check for important directories
    for directory in ['AgricultureWholesale', 'agro', 'account']:
        dir_path = os.path.join(current_dir, directory)
        if os.path.exists(dir_path):
            info[f'{directory}_exists'] = True
            info[f'{directory}_contents'] = os.listdir(dir_path)
        else:
            info[f'{directory}_exists'] = False
    
    return info

def application(environ, start_response):
    """Simple WSGI application that returns debug information"""
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    
    # Collect debug information
    info = debug_info()
    logger.info(f"Debug info: {json.dumps(info, indent=2)}")
    
    response_body = json.dumps(info, indent=2).encode('utf-8')
    
    start_response(status, headers)
    return [response_body]

# Vercel requires the handler to be named 'app'
app = application 