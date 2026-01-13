import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from urllib.parse import urlparse

# Construct the path to the .env file, assuming it's in the 'backend' directory
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for production if .env is not loaded
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./todo_app.db"  # Fallback to local SQLite for development
elif 'neon.tech' in DATABASE_URL:
    # Handle Neon PostgreSQL URL with proper SSL configuration
    try:
        # Parse the URL and ensure proper SSL parameters
        parsed = urlparse(DATABASE_URL)
        if '?sslmode=' not in DATABASE_URL.lower() and 'sslmode' not in DATABASE_URL.lower():
            DATABASE_URL += "?sslmode=require"
    except Exception:
        # If parsing fails, fall back to SQLite
        DATABASE_URL = "sqlite:///./todo_app.db"

engine = create_engine(DATABASE_URL, echo=True)



def get_session():
    with Session(engine) as session:
        yield session
