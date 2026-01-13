from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from typing import List
from ... import schemas, crud
from ...database import get_session
from uuid import UUID

router = APIRouter()

def get_current_user_id(request: Request) -> UUID:
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UUID(user_id)

@router.post(
    "/tasks",
    response_model=schemas.Task,
    responses={
        500: {"model": schemas.HTTPError},
    },
)
def create_task_for_user(
    task: schemas.TaskCreate,
    db: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        return crud.create_task(db=db, task=task, user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/tasks",
    response_model=List[schemas.Task],
    responses={
        500: {"model": schemas.HTTPError},
    },
)
def read_tasks_for_user(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        tasks = crud.get_tasks(db, user_id=user_id, skip=skip, limit=limit)
        return tasks
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/tasks/{task_id}",
    response_model=schemas.Task,
    responses={
        404: {"model": schemas.HTTPError},
        500: {"model": schemas.HTTPError},
    },
)
def read_task_for_user(
    task_id: UUID,
    db: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        db_task = crud.get_task(db, user_id=user_id, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")



@router.put(
    "/tasks/{task_id}",
    response_model=schemas.Task,
    responses={
        404: {"model": schemas.HTTPError},
        500: {"model": schemas.HTTPError},
    },
)
def update_task(
    task_id: UUID,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        db_task = crud.update_task(db, user_id=user_id, task_id=task_id, task=task)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/tasks/{task_id}",
    responses={
        200: {"description": "Task deleted successfully"},
        404: {"model": schemas.HTTPError},
        500: {"model": schemas.HTTPError},
    },
)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        db_task = crud.delete_task(db, user_id=user_id, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
