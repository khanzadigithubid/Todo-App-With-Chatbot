#!/usr/bin/env python
"""
Database reset script to recreate tables with correct schema
"""
import logging
from app.database import engine
from app.models import SQLModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Drop and recreate all tables with the correct schema"""
    try:
        logger.info("Dropping and recreating database tables...")
        
        # Drop all tables
        SQLModel.metadata.drop_all(engine)
        logger.info("All tables dropped successfully")
        
        # Create all tables with the updated schema
        SQLModel.metadata.create_all(engine)
        logger.info("All tables created successfully with updated schema")
        
        # Verify that the user table has the password column
        from sqlmodel import text
        with engine.connect() as conn:
            # Query the user table structure
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'user' AND table_schema = 'public'
            """))
            columns = result.fetchall()
            
            logger.info("Current 'user' table structure:")
            for col in columns:
                logger.info(f"  - {col[0]}: {col[1]}")
                
            # Check if password column exists
            column_names = [col[0] for col in columns]
            if 'password' in column_names:
                logger.info("✓ Password column exists in user table")
            else:
                logger.error("✗ Password column is missing from user table")
                
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    reset_database()
    print("Database reset completed successfully!")