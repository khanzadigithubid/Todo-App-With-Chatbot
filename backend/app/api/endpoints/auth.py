from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt
# import os # Removed
# from dotenv import load_dotenv # Removed

from ...database import get_session
from ... import models, crud, schemas # Import models, crud, and schemas
from ...auth_schemas import Token, UserCreate # Import Token and UserCreate from auth_schemas
from ... import config # Import config

# load_dotenv() # Removed
SECRET_KEY = config.SECRET_KEY # Use SECRET_KEY from config
# print(f"Auth endpoint using SECRET_KEY: {SECRET_KEY}") # Removed
ALGORITHM = config.ALGORITHM # Use ALGORITHM from config
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES # Use ACCESS_TOKEN_EXPIRE_MINUTES from config

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

import logging

logger = logging.getLogger(__name__)

@router.post(
    "/signup",
    response_model=Token,
    responses={
        409: {"model": schemas.HTTPError, "description": "Email already registered"},
        500: {"model": schemas.HTTPError},
    },
)
def signup_user(user: UserCreate, db: Session = Depends(get_session)):
    try:
        logger.info(f"Attempting to create user with email: {user.email}")
        logger.info(f"Received user data: {user}")
        db_user = crud.create_user(db=db, user=user)  # Create user
        logger.info(f"User created successfully with ID: {db_user.id}")

        # After creating the user, generate a token for immediate login
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:  # Fixed: Capture the exception in 'e'
        # Re-raise HTTP exceptions (like 409 for email already registered)
        logger.error(f"HTTPException during signup: {str(e)}")
        raise
    except Exception as e:
        # Log the actual error for debugging - showing the real error instead of masking it
        logger.error(f"Unexpected error during signup: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        # For debugging: return the actual error message instead of generic 500
        raise HTTPException(status_code=500, detail=f"Signup error: {str(e)}")


@router.post(
    "/token",
    response_model=Token,
    responses={
        401: {"model": schemas.HTTPError},
        500: {"model": schemas.HTTPError},
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
):
    try:
        logger.info(f"Attempting login for user: {form_data.username}")
        user = db.exec(
            select(models.User).where(models.User.email == form_data.username)
        ).first()

        if not user or not crud.verify_password(
            form_data.password, user.password
        ):  # Use crud.verify_password
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        logger.info(f"Login successful for user: {user.id}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:  # Fixed: Capture the exception in 'e'
        logger.error(f"HTTPException during login: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

