#!/usr/bin/env python
"""
Enhanced startup script with database readiness check
"""
import uvicorn
import os
import logging
import time
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.database import engine
from app.main import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db(max_attempts=30, delay=1):
    """
    Wait for the database to be ready before starting the server.
    """
    logger.info("Waiting for database to be ready...")
    
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                # Test the connection
                conn.execute(text("SELECT 1"))
                logger.info("Database connection established!")
                return True
        except OperationalError as e:
            logger.warning(f"Attempt {attempt + 1}/{max_attempts}: Database not ready - {e}")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"Unexpected error connecting to database: {e}")
            if attempt == max_attempts - 1:  # Last attempt
                raise
            time.sleep(delay)
    
    raise Exception(f"Database not ready after {max_attempts} attempts")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    try:
        # Wait for database to be ready
        wait_for_db()
        
        logger.info(f"Starting server on {host}:{port}")
        
        # Start the server
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info",  # Set appropriate log level
            workers=1  # Use single worker for development
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        exit(1)