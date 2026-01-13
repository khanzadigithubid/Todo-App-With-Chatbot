import os
from dotenv import load_dotenv
import secrets

# Load environment variables once
load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    # For development only - in production, this should be set as an environment variable
    import warnings
    SECRET_KEY = secrets.token_urlsafe(32)  # Generate a secure random key for development
    warnings.warn(
        "Using generated SECRET_KEY for development. "
        "Please set BETTER_AUTH_SECRET environment variable for production.",
        UserWarning
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# MCP Server Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8080")  # Default MCP server URL
MCP_TIMEOUT = int(os.getenv("MCP_TIMEOUT", "30"))  # Timeout for MCP requests in seconds
MCP_MAX_RETRIES = int(os.getenv("MCP_MAX_RETRIES", "3"))  # Number of retries for failed requests
