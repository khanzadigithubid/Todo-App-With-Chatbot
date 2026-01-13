#!/usr/bin/env python
"""
Test script to verify the backend application starts without errors
"""
import sys
import os
import traceback

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_application_import():
    """Test if the main application can be imported without errors"""
    try:
        print("Testing application import...")
        from backend.app.main import app
        print("✓ Application imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import application: {e}")
        traceback.print_exc()
        return False

def test_database_connection():
    """Test if the database connection works"""
    try:
        print("Testing database connection...")
        from backend.app.database import engine
        from sqlmodel import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        traceback.print_exc()
        return False

def test_models_creation():
    """Test if models can be created"""
    try:
        print("Testing model creation...")
        from backend.app.database import engine
        from backend.app import models
        from sqlmodel import SQLModel
        
        # Try to create all tables
        SQLModel.metadata.create_all(engine)
        print("✓ Models created successfully")
        return True
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("Starting backend application tests...\n")
    
    tests = [
        ("Application Import", test_application_import),
        ("Database Connection", test_database_connection),
        ("Models Creation", test_models_creation),
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
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)