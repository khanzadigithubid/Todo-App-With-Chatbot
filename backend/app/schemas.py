from pydantic import BaseModel, Field
from typing import Optional, List # Added List
from uuid import UUID
from datetime import datetime
from .auth_schemas import UserCreate, Token, TokenData, UserLogin # Import from auth_schemas

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending") # New field
    priority: str = Field(default="medium") # New field
    categories: Optional[List[str]] = None # New field
    is_recurring: bool = Field(default=False) # New field
    recurrence_pattern: Optional[str] = None # New field

class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None # New field

class TaskUpdate(TaskBase):
    title: Optional[str] = None # Allow partial update
    description: Optional[str] = None # Allow partial update
    status: Optional[str] = None # Allow partial update
    priority: Optional[str] = None # Allow partial update
    categories: Optional[List[str]] = None # Allow partial update
    is_recurring: Optional[bool] = None # Allow partial update
    recurrence_pattern: Optional[str] = None # Allow partial update
    due_date: Optional[datetime] = None # Allow partial update

class Task(TaskBase):
    id: UUID # Changed to UUID
    user_id: UUID
    created_at: datetime # New field
    updated_at: datetime # New field
    due_date: Optional[datetime] = None # New field

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    name: str

class HTTPError(BaseModel):
    detail: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: UUID
    created_at: datetime
    tasks: List[Task] = [] # Changed to List

    class Config:
        from_attributes = True
