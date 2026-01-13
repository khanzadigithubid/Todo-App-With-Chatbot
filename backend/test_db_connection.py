import os
import sys
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
from app.database import DATABASE_URL

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

print(f"DATABASE_URL: {DATABASE_URL}", flush=True)

if DATABASE_URL:
    try:
        print("Attempting to create engine...", flush=True)
        engine = create_engine(DATABASE_URL, echo=True)
        print("Engine created successfully!", flush=True)

        # Try to connect
        print("Attempting to connect to database...", flush=True)
        with engine.connect() as conn:
            print("Database connection successful!", flush=True)

        # Create tables
        print("Creating tables...", flush=True)
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully!", flush=True)
    except Exception as e:
        print(f"Database connection failed: {e}", flush=True)
        import traceback
        traceback.print_exc()
else:
    print("DATABASE_URL is not set", flush=True)