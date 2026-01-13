#!/usr/bin/env python
"""
Production startup script for the backend API
Designed for deployment on Hugging Face Spaces
"""
import uvicorn
import os
import logging
from app.main import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    logger.info(f"Starting server on {host}:{port}")

    # Configure uvicorn to run with production settings
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info",  # Set appropriate log level
        workers=1  # Use single worker for development
    )