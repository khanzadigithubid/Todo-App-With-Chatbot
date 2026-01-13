#!/usr/bin/env python3
"""
Verification script to confirm authentication code fixes
"""

import sys
import os

def verify_auth_fixes():
    print("Verifying authentication code fixes...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # 1. Check that jose.jwt is imported instead of jwt
    auth_file_path = os.path.join(backend_dir, 'app', 'api', 'endpoints', 'auth.py')
    with open(auth_file_path, 'r') as f:
        auth_content = f.read()
    
    if 'from jose import jwt' in auth_content:
        print("✓ auth.py correctly imports from jose import jwt")
    else:
        print("✗ auth.py does not import from jose import jwt")
        return False
        
    if 'import jwt' in auth_content and 'from jose import jwt' not in auth_content.replace('from jose import jwt', ''):
        print("✗ auth.py incorrectly imports jwt directly")
        return False
    else:
        print("✓ auth.py does not import jwt directly")
    
    # 2. Check middleware file
    middleware_file_path = os.path.join(backend_dir, 'app', 'middleware.py')
    with open(middleware_file_path, 'r') as f:
        middleware_content = f.read()
    
    if 'from jose import jwt' in middleware_content:
        print("✓ middleware.py correctly imports from jose import jwt")
    else:
        print("✗ middleware.py does not import from jose import jwt")
        return False
        
    if 'import jwt' in middleware_content and 'from jose import jwt' not in middleware_content.replace('from jose import jwt', ''):
        print("✗ middleware.py incorrectly imports jwt directly")
        return False
    else:
        print("✓ middleware.py does not import jwt directly")
    
    # 3. Check requirements.txt
    req_file_path = os.path.join(backend_dir, 'requirements.txt')
    with open(req_file_path, 'r') as f:
        req_content = f.read()
    
    if 'python-jose' in req_content:
        print("✓ requirements.txt includes python-jose")
    else:
        print("✗ requirements.txt does not include python-jose")
        return False
    
    if 'PyJWT' not in req_content:
        print("✓ requirements.txt does not include PyJWT (replaced by python-jose)")
    else:
        print("✗ requirements.txt still includes PyJWT")
        return False
    
    # 4. Check pyproject.toml
    pyproj_file_path = os.path.join(os.path.dirname(__file__), 'pyproject.toml')
    with open(pyproj_file_path, 'r') as f:
        pyproj_content = f.read()
    
    if 'python-jose' in pyproj_content:
        print("✓ pyproject.toml includes python-jose")
    else:
        print("✗ pyproject.toml does not include python-jose")
        return False
    
    if 'PyJWT' not in pyproj_content:
        print("✓ pyproject.toml does not include PyJWT (replaced by python-jose)")
    else:
        print("✗ pyproject.toml still includes PyJWT")
        return False
    
    # 5. Check that passlib[bcrypt] is used
    if 'passlib[bcrypt]' in req_content:
        print("✓ requirements.txt includes passlib[bcrypt]")
    else:
        print("✗ requirements.txt does not include passlib[bcrypt]")
        return False
    
    if 'passlib[bcrypt]' in pyproj_content:
        print("✓ pyproject.toml includes passlib[bcrypt]")
    else:
        print("✗ pyproject.toml does not include passlib[bcrypt]")
        return False
    
    # 6. Check OAuth2 usage
    if 'OAuth2PasswordRequestForm' in auth_content:
        print("✓ auth.py uses OAuth2PasswordRequestForm")
    else:
        print("✗ auth.py does not use OAuth2PasswordRequestForm")
        return False
    
    print("\nAll authentication code fixes verified successfully!")
    return True

if __name__ == "__main__":
    success = verify_auth_fixes()
    if not success:
        sys.exit(1)