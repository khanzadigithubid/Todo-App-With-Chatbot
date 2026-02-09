# backend/crud.py

from sqlmodel import Session, select
from .models import User, Task
from typing import Optional
from uuid import UUID

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_tasks(session: Session, user_id: str, skip: int = 0, limit: int = 100):
    statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    return session.exec(statement).all()

def create_task(session: Session, task: Task) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # Publish task created event to Kafka
    import asyncio
    from .events.kafka_producer import kafka_producer
    asyncio.create_task(
        kafka_producer.publish_task_event(
            event_type="created",
            task_data=task.model_dump(),
            user_id=str(task.user_id)
        )
    )
    
    return task

def get_task(session: Session, task_id: UUID, user_id: str) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()

def update_task(session: Session, task_id: UUID, task: Task, user_id: str) -> Optional[Task]:
    existing_task = session.get(Task, task_id)
    if existing_task and existing_task.user_id == user_id:
        # Store original status to detect completion
        original_status = existing_task.status
        
        # Update the task with provided fields
        for field, value in task.model_dump(exclude_unset=True).items():
            if field != "id":  # Don't update the ID
                setattr(existing_task, field, value)
        session.add(existing_task)
        session.commit()
        session.refresh(existing_task)
        
        # Publish task updated event to Kafka
        import asyncio
        from .events.kafka_producer import kafka_producer
        asyncio.create_task(
            kafka_producer.publish_task_event(
                event_type="updated",
                task_data=existing_task.model_dump(),
                user_id=user_id
            )
        )
        
        # Check if task was completed and it's a recurring task
        if original_status != "completed" and existing_task.status == "completed" and existing_task.is_recurring:
            # This will be handled by the Kafka consumer
            pass
        
        return existing_task
    return None

def delete_task(session: Session, task_id: UUID, user_id: str) -> bool:
    task = session.get(Task, task_id)
    if task and task.user_id == user_id:
        # Publish task deleted event to Kafka
        import asyncio
        from .events.kafka_producer import kafka_producer
        asyncio.create_task(
            kafka_producer.publish_task_event(
                event_type="deleted",
                task_data=task.model_dump(),
                user_id=user_id
            )
        )
        
        session.delete(task)
        session.commit()
        return True
    return False

def get_password_hash(password: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)