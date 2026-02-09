# backend/api/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...database import get_session
from ...models import User
from ...auth_schemas import UserLogin, Token
from ...crud import get_user_by_email
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    secret = os.getenv("BETTER_AUTH_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server configuration error")
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
    return encoded_jwt

@router.post("/token", response_model=Token)
def login_for_access_token(user_credentials: UserLogin, session: Session = Depends(get_session)):
    user = authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)  # Token expires in 30 minutes
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}