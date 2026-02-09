# backend/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending", max_length=20)
    priority: str = Field(default="medium", max_length=20)
    categories: Optional[list[str]] = Field(default=None, sa_column=Column(JSON))
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    due_date: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user: User = Relationship(back_populates="tasks")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Store as string since we're using UUID from JWT
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    messages: list["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Store as string since we're using UUID from JWT
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    conversation: Conversation = Relationship(back_populates="messages")