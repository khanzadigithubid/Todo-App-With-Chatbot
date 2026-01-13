#!/usr/bin/env python
"""
Minimal test server to isolate the internal server error
"""
import logging
import sys
import os

# Set up logging to see what's happening
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_minimal_app():
    """Test creating a minimal FastAPI app to isolate the issue"""
    try:
        logger.info("Starting minimal app test...")
        
        # Import minimal dependencies first
        logger.info("Importing FastAPI...")
        from fastapi import FastAPI
        logger.info("✓ FastAPI imported successfully")
        
        # Create a minimal app
        logger.info("Creating minimal app...")
        app = FastAPI()
        
        @app.get("/")
        def root():
            return {"message": "Server is running"}
        
        logger.info("✓ Minimal app created successfully")
        
        # Try to import and configure the real app components one by one
        logger.info("Testing database configuration...")
        try:
            from backend.app.database import engine
            logger.info("✓ Database engine created successfully")
        except Exception as e:
            logger.error(f"Database configuration error: {e}")
            return False
            
        logger.info("Testing models import...")
        try:
            from backend.app import models
            logger.info("✓ Models imported successfully")
        except Exception as e:
            logger.error(f"Models import error: {e}")
            return False
            
        logger.info("Testing schemas import...")
        try:
            from backend.app import schemas
            logger.info("✓ Schemas imported successfully")
        except Exception as e:
            logger.error(f"Schemas import error: {e}")
            return False
            
        logger.info("Testing CRUD operations import...")
        try:
            from backend.app import crud
            logger.info("✓ CRUD operations imported successfully")
        except Exception as e:
            logger.error(f"CRUD operations import error: {e}")
            return False
            
        logger.info("Testing config import...")
        try:
            from backend.app import config
            logger.info("✓ Config imported successfully")
        except Exception as e:
            logger.error(f"Config import error: {e}")
            return False
            
        logger.info("Testing tools import...")
        try:
            from backend.app.tools.registry import tool_registry
            logger.info("✓ Tools registry imported successfully")
        except Exception as e:
            logger.error(f"Tools registry import error: {e}")
            return False
            
        logger.info("All components imported successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in minimal app test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting backend diagnostic test...")
    success = test_minimal_app()
    
    if success:
        logger.info("🎉 Diagnostic test PASSED - No obvious issues found")
        logger.info("The issue might be related to runtime conditions rather than imports")
    else:
        logger.error("❌ Diagnostic test FAILED - Issues found")