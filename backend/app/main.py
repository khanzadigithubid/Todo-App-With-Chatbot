import os
from dotenv import load_dotenv
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from uuid import UUID
from .database import engine, get_session
from . import models, schemas
from .api.endpoints import tasks, users, auth, chat
from .middleware import JWTAuthMiddleware
from . import config
from .crud import get_password_hash

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware with comprehensive configuration
# Get allowed origins from environment variable or use defaults
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()] if allowed_origins_env else []

# Add default development origins
default_origins = [
    "http://localhost:3000",      # Next.js default port
    "http://127.0.0.1:3000",     # Next.js default port (IPv4)
    "http://localhost:3001",      # Alternative Next.js port
    "http://127.0.0.1:3001",     # Alternative Next.js port (IPv4)
    "http://localhost:8000",      # Backend server (for direct testing)
    "http://127.0.0.1:8000",     # Backend server (IPv4)
    "https://localhost:3000",     # HTTPS (if using)
    "https://127.0.0.1:3000",    # HTTPS (IPv4)
    "http://localhost:3002",      # Additional Next.js port
    "http://127.0.0.1:3002",     # Additional Next.js port (IPv4)
    "http://localhost:3003",      # Additional Next.js port
    "http://127.0.0.1:3003",     # Additional Next.js port (IPv4)
    "http://localhost:3004",      # Additional Next.js port
    "http://127.0.0.1:3004",     # Additional Next.js port (IPv4)
    "http://localhost:3005",      # Additional Next.js port
    "http://127.0.0.1:3005",     # Additional Next.js port (IPv4)
    "http://localhost:3006",      # Additional Next.js port
    "http://127.0.0.1:3006",     # Additional Next.js port (IPv4)
    "http://localhost:3007",      # Additional Next.js port
    "http://127.0.0.1:3007",     # Additional Next.js port (IPv4)
    "http://localhost:3008",      # Additional Next.js port
    "http://127.0.0.1:3008",     # Additional Next.js port (IPv4)
    "http://localhost:3009",      # Additional Next.js port
    "http://127.0.0.1:3009",     # Additional Next.js port (IPv4)
    "http://localhost:3010",      # Additional Next.js port
    "http://127.0.0.1:3010",     # Additional Next.js port (IPv4)
    "https://*.vercel.app",       # Vercel deployments
]

# Combine default and environment-specific origins
all_origins = default_origins + allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    # Expose authorization header to frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization", "Content-Type", "X-Requested-With"],
)

# Add JWT middleware
app.add_middleware(JWTAuthMiddleware)


@app.on_event("startup")
def on_startup():
    try:
        logger.info("Initializing database tables...")
        # Attempt to create tables with a connection test first
        with engine.connect() as conn:
            logger.info("Database connection successful")

        # Create tables
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise


app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])  # Tasks endpoints already include /tasks in their definition
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"Hello": "World"}