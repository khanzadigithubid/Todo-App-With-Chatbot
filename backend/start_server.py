# backend/start_server.py

import uvicorn
import os
from .main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        debug=True
    )