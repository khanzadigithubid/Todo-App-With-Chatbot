from sqlmodel import Session, select
from datetime import datetime, timezone
from uuid import UUID
from . import models, schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext 
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Truncate the password to 72 characters before hashing to avoid bcrypt's 72-byte limit
    truncated_password = password[:72] if password else ""
    return pwd_context.hash(truncated_password)

def create_user(db: Session, user: schemas.UserCreate):
    # Check if user with this email already exists
    existing_user = db.exec(select(models.User).where(models.User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed_password = get_password_hash(user.password) # Hash the password
    db_user = models.User(email=user.email, name=user.name, password=hashed_password) # Store hashed password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_task(db: Session, task: schemas.TaskCreate, user_id: UUID):
    try:
        db_task = models.Task(**task.dict(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        logging.error(f"Error creating task: {str(e)}", exc_info=True)
        raise

def get_tasks(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    statement = select(models.Task).where(models.Task.user_id == user_id).offset(skip).limit(limit)
    results = db.exec(statement)
    return results.fetchall()

def get_task(db: Session, task_id: UUID, user_id: UUID): # Changed task_id type to UUID
    statement = select(models.Task).where(models.Task.id == task_id, models.Task.user_id == user_id)
    result = db.exec(statement)
    return result.first()

def update_task(db: Session, task_id: UUID, task: schemas.TaskUpdate, user_id: UUID): # Changed task_id type to UUID
    db_task = get_task(db, task_id, user_id)
    if db_task:
        task_data = task.dict(exclude_unset=True)
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: UUID, user_id: UUID): # Changed task_id type to UUID
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task