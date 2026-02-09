# backend/main.py

import os
from dotenv import load_dotenv
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from backend.database import engine
from backend.api.endpoints import tasks, users, auth, chat
from backend.middleware import JWTAuthMiddleware

# Import Kafka components
from backend.events.kafka_producer import init_kafka_producer, close_kafka_producer
from backend.events.kafka_consumer import init_kafka_consumer, close_kafka_consumer

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware with comprehensive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
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
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    # Expose authorization header to frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization", "Content-Type", "X-Requested-With"],
)

# Add JWT middleware
app.add_middleware(JWTAuthMiddleware)


@app.on_event("startup")
async def on_startup():
    try:
        logger.info("Initializing database tables...")
        # Attempt to create tables with a connection test first
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables initialized successfully")
        
        # Initialize Kafka producer and consumer
        logger.info("Initializing Kafka producer and consumer...")
        await init_kafka_producer()
        await init_kafka_consumer()
        logger.info("Kafka producer and consumer initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing application: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise


@app.on_event("shutdown")
async def on_shutdown():
    try:
        logger.info("Shutting down Kafka producer and consumer...")
        await close_kafka_producer()
        await close_kafka_consumer()
        logger.info("Kafka producer and consumer shut down successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")


app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"Hello": "World"}