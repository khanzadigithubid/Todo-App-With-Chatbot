from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt
import logging
# import os # Removed
# from dotenv import load_dotenv # Removed
from . import config # Import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load_dotenv() # Removed

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS requests to pass through for CORS preflight
        if request.method == "OPTIONS":
            return await call_next(request)

        # Define unprotected routes that should be accessible without authentication
        unprotected_routes = [
            "/api/token",           # Login endpoint
            "/api/users/",          # User creation endpoint
            "/api/users",           # User creation endpoint
            "/api/signup",          # Signup endpoint
            "/",                    # Root endpoint
        ]

        if request.url.path.startswith("/api/"):
            # Check if the current path is in the list of unprotected routes
            is_unprotected = any(
                request.url.path == route or
                request.url.path.startswith(route + "/") and route != "/"
                for route in unprotected_routes
            )

            if not is_unprotected:
                auth_header = request.headers.get("Authorization")
                if not auth_header or not auth_header.startswith("Bearer "):
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Unauthorized"}
                    )

                token = auth_header.split(" ")[1]
                try:
                    # secret_key = os.environ.get("BETTER_AUTH_SECRET") # Removed
                    secret_key = config.SECRET_KEY # Use SECRET_KEY from config
                    payload = jwt.decode(token, secret_key, algorithms=[config.ALGORITHM]) # Use ALGORITHM from config
                    request.state.user_id = payload.get("sub")

                    # Validate that the user_id is a valid UUID
                    from uuid import UUID
                    try:
                        UUID(request.state.user_id)
                    except (ValueError, TypeError):
                        return JSONResponse(
                            status_code=401,
                            content={"detail": "Invalid token payload"}
                        )

                except jwt.ExpiredSignatureError:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Token has expired"}
                    )
                except jwt.JWTError:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid token"}
                    )
                except Exception as e:
                    logger.error(f"Unexpected error during JWT validation: {e}")
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Authentication error"}
                    )

        response = await call_next(request)
        return response
