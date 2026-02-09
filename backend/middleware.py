# backend/middleware.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from datetime import datetime
import os

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for certain endpoints
        if request.url.path in ["/", "/docs", "/redoc", "/openapi.json", "/api/auth/token", "/api/users"]:
            response = await call_next(request)
            return response

        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Extract the token
        token = auth_header.split(" ")[1]

        # Get the secret key
        secret = os.getenv("BETTER_AUTH_SECRET")
        if not secret:
            raise HTTPException(status_code=500, detail="Server configuration error")

        try:
            # Decode the JWT token
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(status_code=401, detail="Could not validate credentials")

            # Add user info to request state
            request.state.user_id = user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        response = await call_next(request)
        return response