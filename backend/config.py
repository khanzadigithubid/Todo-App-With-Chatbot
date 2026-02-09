# backend/config.py

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-in-production")

settings = Settings()