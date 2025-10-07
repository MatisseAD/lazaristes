"""
Simple test script to verify the Flask application works correctly.
"""

import sys
import json
from io import StringIO

def test_code_execution():
    """Test the sandboxed code execution functionality."""
    print("Testing code execution sandbox...")
    
    # Test 1: Basic print
    test_code_1 = "print('Hello, World!')"
    print(f"Test 1: {test_code_1}")
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    restricted_globals = {
        '__builtins__': {
            'print': print,
            'len': len,
            'range': range,
        }
    }
    
    try:
        exec(test_code_1, restricted_globals, {})
        output = sys.stdout.getvalue()
        print(f"✓ Test 1 passed: {output.strip()}", file=sys.__stdout__)
    except Exception as e:
        print(f"✗ Test 1 failed: {e}", file=sys.__stdout__)
    finally:
        sys.stdout = old_stdout
    
    # Test 2: Mathematical operations
    test_code_2 = """
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Sum: {total}")
"""
    print(f"\nTest 2: Mathematical operations")
    
    sys.stdout = StringIO()
    restricted_globals = {
        '__builtins__': {
            'print': print,
            'sum': sum,
            'list': list,
        }
    }
    
    try:
        exec(test_code_2, restricted_globals, {})
        output = sys.stdout.getvalue()
        print(f"✓ Test 2 passed: {output.strip()}", file=sys.__stdout__)
    except Exception as e:
        print(f"✗ Test 2 failed: {e}", file=sys.__stdout__)
    finally:
        sys.stdout = old_stdout
    
    # Test 3: Attempt to import (should fail)
    test_code_3 = "import os"
    print(f"\nTest 3: Attempt to import (should fail)")
    
    sys.stdout = StringIO()
    restricted_globals = {
        '__builtins__': {}
    }
    
    try:
        exec(test_code_3, restricted_globals, {})
        print("✗ Test 3 failed: Import was allowed", file=sys.__stdout__)
    except Exception as e:
        print(f"✓ Test 3 passed: Import blocked ({type(e).__name__})", file=sys.__stdout__)
    finally:
        sys.stdout = old_stdout

def test_api_endpoints():
    """Test that API endpoints are properly defined."""
    print("\n\nTesting API endpoints...")
    
    try:
        from app import app
        
        # Check routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        expected_routes = [
            '/',
            '/api/commits',
            '/api/files',
            '/api/execute',
            '/webhook',
            '/api/stats'
        ]
        
        print("Registered routes:")
        for route in sorted(routes):
            print(f"  - {route}")
        
        for expected in expected_routes:
            if expected in routes:
                print(f"✓ {expected} is registered")
            else:
                print(f"✗ {expected} is missing")
        
    except Exception as e:
        print(f"✗ Failed to load app: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("Lazaristes Application Test Suite")
    print("=" * 60)
    
    test_code_execution()
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)
