# backend/api/endpoints/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from ...database import get_session
from ...models import Task
from ...auth_schemas import UserLogin
from ...crud import get_tasks, create_task, get_task, update_task, delete_task
from typing import List

router = APIRouter()

def get_current_user_id(request):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UUID(user_id)

@router.get("/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 100, user_id: UUID = Depends(get_current_user_id), session: Session = Depends(get_session)):
    tasks = get_tasks(session, user_id=str(user_id), skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=Task)
def create_new_task(task: Task, user_id: UUID = Depends(get_current_user_id), session: Session = Depends(get_session)):
    task.user_id = user_id
    return create_task(session, task)

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: UUID, user_id: UUID = Depends(get_current_user_id), session: Session = Depends(get_session)):
    task = get_task(session, task_id=task_id, user_id=str(user_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_existing_task(task_id: UUID, task: Task, user_id: UUID = Depends(get_current_user_id), session: Session = Depends(get_session)):
    updated_task = update_task(session, task_id=task_id, task=task, user_id=str(user_id))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
def delete_existing_task(task_id: UUID, user_id: UUID = Depends(get_current_user_id), session: Session = Depends(get_session)):
    deleted = delete_task(session, task_id=task_id, user_id=str(user_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}