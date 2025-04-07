import json
import os
import sys


def application(environ, start_response):
    """Simple WSGI application that returns diagnostic information"""
    
    # Build debug information
    info = {
        'message': 'Diagnostic page for AgricultureWholesale',
        'python_version': sys.version,
        'sys_path': sys.path,
        'working_directory': os.getcwd(),
        'environment_variables': {k: v for k, v in os.environ.items() 
                                 if not k.startswith(('AWS_', 'LAMBDA'))},
    }
    
    # Check directory contents
    try:
        info['directory_contents'] = os.listdir('.')
        
        # Check for key directories
        for dir_name in ['AgricultureWholesale', 'agro', 'account']:
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                info[f'{dir_name}_exists'] = True
                info[f'{dir_name}_contents'] = os.listdir(dir_name)
            else:
                info[f'{dir_name}_exists'] = False
    except Exception as e:
        info['directory_error'] = str(e)
    
    # Convert to JSON string
    response_body = json.dumps(info, indent=2).encode('utf-8')
    
    # Set response headers
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, headers)
    return [response_body]

# For Vercel
app = application 