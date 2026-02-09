from fastapi import APIRouter
from . import tasks, chat

router = APIRouter()
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])