from sqlmodel import SQLModel, Field, Relationship, JSON # Keep JSON import for Field(JSON)
from typing import Optional, List # Added List import
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column # Import Column from sqlalchemy
from sqlalchemy.dialects.postgresql import JSON # Import JSON from sqlalchemy.dialects.postgresql if using PostgreSQL specific JSON type

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True) # Changed from int to UUID
    user_id: UUID = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending", max_length=20) # Replaced completed: bool, added max_length
    priority: str = Field(default="medium", max_length=20) # New field, added max_length
    categories: Optional[List[str]] = Field(default=None, sa_column=Column(JSON)) # Corrected for JSON storage
    is_recurring: bool = Field(default=False) # New field
    recurrence_pattern: Optional[str] = Field(default=None, max_length=20) # New field, added max_length
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    due_date: Optional[datetime] = None # New field
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False) # Updated to be more compatible
    user: User = Relationship(back_populates="tasks")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Store as string since we're using UUID from JWT
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Store as string since we're using UUID from JWT
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    conversation: Conversation = Relationship(back_populates="messages")
