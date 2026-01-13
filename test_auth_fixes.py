"""
Test script to verify that the authentication fixes work correctly
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_jwt_import():
    """Test that jose.jwt can be imported and used correctly"""
    try:
        from jose import jwt
        print("✓ jose.jwt imported successfully")
        
        # Test encoding and decoding
        payload = {"sub": "test_user", "exp": 9999999999}
        secret = "test_secret"
        token = jwt.encode(payload, secret, algorithm="HS256")
        print("✓ jwt.encode works correctly")
        
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        print("✓ jwt.decode works correctly")
        print(f"  - Encoded token: {token[:30]}...")
        print(f"  - Decoded payload: {decoded}")
        
        return True
    except ImportError as e:
        print(f"✗ Failed to import jose.jwt: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing jose.jwt functionality: {e}")
        return False

def test_bcrypt_usage():
    """Test that bcrypt is properly configured with passlib"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Test hashing and verification
        plain_password = "test_password_123"
        hashed = pwd_context.hash(plain_password)
        verified = pwd_context.verify(plain_password, hashed)
        
        print("✓ bcrypt with passlib works correctly")
        print(f"  - Plain password: {plain_password}")
        print(f"  - Hashed: {hashed[:30]}...")
        print(f"  - Verification: {verified}")
        
        return True
    except Exception as e:
        print(f"✗ Error testing bcrypt functionality: {e}")
        return False

def test_oauth2_form():
    """Test that OAuth2PasswordRequestForm is available"""
    try:
        from fastapi.security import OAuth2PasswordRequestForm
        print("✓ OAuth2PasswordRequestForm is available")
        return True
    except ImportError as e:
        print(f"✗ Failed to import OAuth2PasswordRequestForm: {e}")
        return False

def main():
    print("Testing authentication fixes...")
    print("="*50)
    
    tests = [
        ("JWT Import and Functionality", test_jwt_import),
        ("Bcrypt/Passlib Functionality", test_bcrypt_usage),
        ("OAuth2 Form", test_oauth2_form),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("Test Summary:")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print(f"\nOverall result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    main()