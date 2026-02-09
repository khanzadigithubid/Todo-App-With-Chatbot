from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from ...database import get_session
from sqlmodel import Session, select
from ...models import Task
from ...auth_schemas import get_current_user_id

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    category: Optional[str] = None
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[str] = None

@router.get("/")
async def get_tasks(
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Get all tasks for the authenticated user
    tasks = session.exec(select(Task).where(Task.user_id == str(user_id))).all()
    return tasks

@router.post("/")
async def create_task(
    task: TaskCreate,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Create a new task for the authenticated user
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        category=task.category,
        due_date=task.due_date,
        user_id=str(user_id)
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/{task_id}")
async def get_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Get a specific task for the authenticated user
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task

@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Update a task for the authenticated user
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Update the task with provided fields
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Delete a task for the authenticated user
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/complete")
async def toggle_task_completion(
    task_id: int,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Toggle task completion status for the authenticated user
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task