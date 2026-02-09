from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field
from uuid import UUID
from fastapi import Request, HTTPException
from jwt import decode, DecodeError
from datetime import datetime
import os

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: UUID | None = None

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

def get_current_user_id(request: Request) -> UUID:
    """
    Extract the user ID from the JWT token in the Authorization header
    """
    # Get the authorization header
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
        payload = decode(token, secret, algorithms=["HS256"])
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        return UUID(user_id)
    except DecodeError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")
