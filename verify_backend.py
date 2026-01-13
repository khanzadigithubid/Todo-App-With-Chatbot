#!/usr/bin/env python
"""
Simple test to verify the backend application can start without errors
"""
import sys
import os
import traceback

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_basic_imports():
    """Test basic imports to catch common issues"""
    try:
        print("Testing basic imports...")
        
        # Test core dependencies
        import fastapi
        print("✓ FastAPI imported successfully")
        
        import sqlmodel
        print("✓ SQLModel imported successfully")
        
        import uvicorn
        print("✓ Uvicorn imported successfully")
        
        # Test backend modules
        from backend.app.database import DATABASE_URL, engine
        print(f"✓ Database module imported, URL: {'SET' if DATABASE_URL else 'NOT SET'}")
        
        from backend.app.main import app
        print("✓ Main app imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connection"""
    try:
        print("\nTesting database connection...")
        from backend.app.database import engine
        
        # Try a simple connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_app_startup():
    """Test the app startup event"""
    try:
        print("\nTesting app startup event...")
        from backend.app.main import on_startup
        
        # Call the startup function
        on_startup()
        print("✓ App startup event executed successfully")
        return True
    except Exception as e:
        print(f"✗ App startup event failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("Starting backend verification tests...\n")
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Database Connection", test_database_connection),
        ("App Startup Event", test_app_startup),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("Test Results:")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("="*50)
    if all_passed:
        print("✓ All tests passed! The backend should work correctly.")
        print("\nTo start the server, run:")
        print("cd backend && python run.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)