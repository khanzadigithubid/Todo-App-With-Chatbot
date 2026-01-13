#!/usr/bin/env python
"""
Database patch script to add missing password column if it doesn't exist
"""
import logging
from app.database import engine
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def patch_database():
    """Add missing password column to user table if it doesn't exist"""
    try:
        logger.info("Checking and patching database schema...")
        
        with engine.connect() as conn:
            # Check if password column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user' AND column_name = 'password'
            """))
            
            if result.fetchone() is None:
                # Password column doesn't exist, add it
                logger.info("Password column not found, adding it to user table...")
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN \"password\" TEXT"))
                conn.commit()
                logger.info("Password column added successfully")
            else:
                logger.info("Password column already exists")
        
        logger.info("Database patch completed successfully")
        
    except Exception as e:
        logger.error(f"Error patching database: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    patch_database()
    print("Database patch completed successfully!")