# backend/api/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...database import get_session
from ...models import User
from ...auth_schemas import UserCreate
from ...crud import create_user, get_user_by_email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

@router.post("/")
def create_user_endpoint(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create the user
    db_user = User(email=user.email, password=hashed_password, name=user.name)
    created_user = create_user(session, db_user)
    
    # Return token data (simplified for this example)
    return {
        "id": created_user.id,
        "email": created_user.email,
        "name": created_user.name
    }