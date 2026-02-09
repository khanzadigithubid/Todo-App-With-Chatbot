# backend/services/reminders.py

from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from ..models import Task
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

def get_upcoming_reminders(session: Session, minutes_ahead: int = 5) -> List[Task]:
    """
    Get tasks that have due dates coming up within the specified minutes
    """
    time_threshold = datetime.utcnow() + timedelta(minutes=minutes_ahead)
    
    # Find tasks that are due soon but not yet completed
    upcoming_tasks = session.exec(
        select(Task)
        .where(Task.due_date <= time_threshold)
        .where(Task.status != "completed")
    ).all()
    
    return upcoming_tasks

def get_overdue_tasks(session: Session) -> List[Task]:
    """
    Get tasks that are past their due date and not yet completed
    """
    now = datetime.utcnow()
    
    overdue_tasks = session.exec(
        select(Task)
        .where(Task.due_date < now)
        .where(Task.status != "completed")
    ).all()
    
    return overdue_tasks

def schedule_reminder(task_id: UUID, remind_at: datetime, user_id: str):
    """
    Schedule a reminder for a specific task at a specific time
    This would typically integrate with a job scheduler or Kafka topic
    """
    # In a real implementation, this would schedule a job or publish to a Kafka topic
    # For now, we'll just log the scheduled reminder
    logger.info(f"Scheduled reminder for task {task_id} at {remind_at} for user {user_id}")

def check_and_send_reminders(session: Session):
    """
    Check for upcoming tasks and send reminders
    This would typically be called by a periodic job
    """
    upcoming_tasks = get_upcoming_reminders(session, minutes_ahead=5)
    
    for task in upcoming_tasks:
        # In a real implementation, this would send a notification to the user
        # via email, push notification, etc.
        logger.info(f"Sending reminder for task '{task.title}' due at {task.due_date}")
        
        # Here you would typically publish to a Kafka topic for the notification service
        # to handle