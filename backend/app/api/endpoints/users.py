from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ... import schemas, crud, models # Import models
from ...database import get_session
from uuid import UUID
from ...auth_schemas import UserCreate, Token # Import UserCreate and Token from auth_schemas
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES # Import from auth.py
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post(
    "/",
    response_model=Token,
    responses={
        409: {"model": schemas.HTTPError, "description": "Email already registered"},
        500: {"model": schemas.HTTPError},
    },
)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    try:
        db_user = crud.create_user(db=db, user=user)  # Create user

        # After creating the user, generate a token for immediate login
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already registered")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # In production, log the error `e` to a logging service
        import traceback
        print(f"Error in create_user: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")