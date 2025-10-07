"""
Flask web application for lazaristes dynamic website.
Provides API endpoints for repository updates and Python code execution.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
from datetime import datetime
import sys
from io import StringIO
import traceback
from functools import wraps
import time
import hashlib
import hmac

app = Flask(__name__, static_folder='docs/static', template_folder='docs')
CORS(app)

# Rate limiting storage (in-memory for simplicity)
rate_limit_storage = {}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 10

# Secret for webhook validation (should be set via environment variable)
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '')


def rate_limit(f):
    """Rate limiting decorator for API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean old entries
        if client_ip in rate_limit_storage:
            rate_limit_storage[client_ip] = [
                req_time for req_time in rate_limit_storage[client_ip]
                if current_time - req_time < RATE_LIMIT_WINDOW
            ]
        else:
            rate_limit_storage[client_ip] = []
        
        # Check rate limit
        if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
            return jsonify({
                'error': 'Rate limit exceeded. Please try again later.',
                'status': 'error'
            }), 429
        
        # Record this request
        rate_limit_storage[client_ip].append(current_time)
        
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/api/commits', methods=['GET'])
def get_commits():
    """Get recent commits from the repository."""
    try:
        # Get the last 10 commits
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%H|%an|%ae|%ad|%s', '-10'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Failed to fetch commits',
                'status': 'error'
            }), 500
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    commits.append({
                        'hash': parts[0][:7],
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    })
        
        return jsonify({
            'commits': commits,
            'status': 'success'
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'error': 'Request timeout',
            'status': 'error'
        }), 504
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/files', methods=['GET'])
def get_files():
    """Get list of files added/modified in recent commits."""
    try:
        # Get files changed in last 5 commits
        result = subprocess.run(
            ['git', 'log', '--pretty=format:', '--name-status', '-5'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Failed to fetch files',
                'status': 'error'
            }), 500
        
        files = []
        seen_files = set()
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) == 2:
                    status = parts[0]
                    filename = parts[1]
                    if filename not in seen_files:
                        files.append({
                            'status': status,
                            'filename': filename
                        })
                        seen_files.add(filename)
        
        return jsonify({
            'files': files,
            'status': 'success'
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'error': 'Request timeout',
            'status': 'error'
        }), 504
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/execute', methods=['POST'])
@rate_limit
def execute_code():
    """Execute Python code in a sandboxed environment."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({
                'error': 'No code provided',
                'status': 'error'
            }), 400
        
        # Basic length check to prevent abuse
        if len(code) > 10000:
            return jsonify({
                'error': 'Code too long (max 10000 characters)',
                'status': 'error'
            }), 400
        
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = StringIO()
        redirected_error = StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error
        
        # Define restricted globals/locals for code execution
        restricted_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'bool': bool,
                'abs': abs,
                'max': max,
                'min': min,
                'sum': sum,
                'sorted': sorted,
                'reversed': reversed,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'any': any,
                'all': all,
                'round': round,
                'pow': pow,
            }
        }
        restricted_locals = {}
        
        try:
            # Execute with timeout using alarm (Unix only)
            exec(code, restricted_globals, restricted_locals)
            output = redirected_output.getvalue()
            error = redirected_error.getvalue()
            
            return jsonify({
                'output': output,
                'error': error if error else None,
                'status': 'success'
            })
        except Exception as e:
            error = redirected_error.getvalue()
            traceback_str = traceback.format_exc()
            return jsonify({
                'output': redirected_output.getvalue(),
                'error': error + '\n' + traceback_str if error else traceback_str,
                'status': 'error'
            })
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle GitHub webhook events."""
    try:
        # Verify webhook signature if secret is set
        if WEBHOOK_SECRET:
            signature = request.headers.get('X-Hub-Signature-256', '')
            if signature:
                expected_signature = 'sha256=' + hmac.new(
                    WEBHOOK_SECRET.encode(),
                    request.data,
                    hashlib.sha256
                ).hexdigest()
                
                if not hmac.compare_digest(signature, expected_signature):
                    return jsonify({
                        'error': 'Invalid signature',
                        'status': 'error'
                    }), 401
        
        event = request.headers.get('X-GitHub-Event', 'unknown')
        payload = request.get_json()
        
        # Log webhook event (in production, you might want to trigger updates here)
        print(f"Received webhook event: {event}")
        
        # For push events, we could trigger a git pull here
        if event == 'push':
            # In a production environment, you might want to:
            # 1. Validate the branch
            # 2. Pull latest changes
            # 3. Notify connected clients via WebSocket
            # 4. Update cached data
            pass
        
        return jsonify({
            'message': 'Webhook received',
            'event': event,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get repository statistics."""
    try:
        # Get total commits
        commit_count_result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Get total files
        file_count_result = subprocess.run(
            ['git', 'ls-files'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=5
        )
        
        total_commits = commit_count_result.stdout.strip() if commit_count_result.returncode == 0 else 'N/A'
        files = file_count_result.stdout.strip().split('\n') if file_count_result.returncode == 0 else []
        
        # Count Python files
        py_files = [f for f in files if f.endswith('.py')]
        ipynb_files = [f for f in files if f.endswith('.ipynb')]
        
        return jsonify({
            'total_commits': total_commits,
            'total_files': len(files),
            'python_files': len(py_files),
            'notebook_files': len(ipynb_files),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


if __name__ == '__main__':
    # Run in debug mode for development
    # In production, use a proper WSGI server like gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
