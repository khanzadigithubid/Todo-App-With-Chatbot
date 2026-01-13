#!/usr/bin/env python
"""
Test script to diagnose JWT import issue
"""

def test_jwt_import():
    try:
        import jwt
        print(f"JWT module imported successfully: {jwt}")
        print(f"JWT module location: {jwt.__file__ if hasattr(jwt, '__file__') else 'Built-in or unknown location'}")
        print(f"JWT module attributes: {[attr for attr in dir(jwt) if not attr.startswith('_')]}")
        
        # Check if encode and decode functions exist
        if hasattr(jwt, 'encode'):
            print("✓ jwt.encode function exists")
        else:
            print("✗ jwt.encode function does NOT exist")
            
        if hasattr(jwt, 'decode'):
            print("✓ jwt.decode function exists")
        else:
            print("✗ jwt.decode function does NOT exist")
            
        # Try to use encode and decode
        try:
            import datetime
            payload = {"sub": "test", "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
            token = jwt.encode(payload, "secret", algorithm="HS256")
            print(f"✓ jwt.encode works: {token[:30]}...")
        except Exception as e:
            print(f"✗ jwt.encode failed: {e}")
            
        try:
            decoded = jwt.decode(token, "secret", algorithms=["HS256"])
            print(f"✓ jwt.decode works: {decoded}")
        except Exception as e:
            print(f"✗ jwt.decode failed: {e}")
            
    except ImportError as e:
        print(f"Failed to import jwt module: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing JWT import and functionality...")
    test_jwt_import()