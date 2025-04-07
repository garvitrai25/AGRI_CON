import json
import os
import sys

from flask import Flask, jsonify

# Create Flask app
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Return debug information instead of trying to use Django"""
    
    # Build debug information
    info = {
        'message': 'Diagnostic page for AgricultureWholesale',
        'path_requested': path,
        'environment': {
            'python_version': sys.version,
            'sys_path': sys.path,
            'working_directory': os.getcwd(),
            'environment_variables': {k: v for k, v in os.environ.items() 
                                     if not k.startswith(('AWS_', 'LAMBDA'))},
        }
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
    
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True) 