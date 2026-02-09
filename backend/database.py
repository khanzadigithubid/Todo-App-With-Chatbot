# backend/database.py

from sqlmodel import create_engine, Session
from .config import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session