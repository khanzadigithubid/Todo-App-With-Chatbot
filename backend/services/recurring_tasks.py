# backend/services/recurring_tasks.py

from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from ..models import Task
from uuid import UUID
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class RecurrencePattern(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

def create_next_occurrence(session: Session, original_task: Task) -> Optional[Task]:
    """
    Creates the next occurrence of a recurring task based on its recurrence pattern
    """
    if not original_task.is_recurring or not original_task.recurrence_pattern:
        return None
    
    # Check if the task has reached its end date
    if original_task.recurrence_end_date and datetime.utcnow() > original_task.recurrence_end_date:
        logger.info(f"Recurring task {original_task.id} has reached its end date")
        return None
    
    # Calculate the next due date based on the recurrence pattern
    next_due_date = calculate_next_due_date(original_task.due_date, original_task.recurrence_pattern)
    
    if next_due_date and (not original_task.recurrence_end_date or next_due_date <= original_task.recurrence_end_date):
        # Create a new task with the same properties as the original
        new_task = Task(
            user_id=original_task.user_id,
            title=original_task.title,
            description=original_task.description,
            status="pending",
            priority=original_task.priority,
            categories=original_task.categories,
            is_recurring=original_task.is_recurring,
            recurrence_pattern=original_task.recurrence_pattern,
            recurrence_end_date=original_task.recurrence_end_date,
            due_date=next_due_date
        )
        
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        
        logger.info(f"Created next occurrence of recurring task: {new_task.id}")
        return new_task
    
    return None

def calculate_next_due_date(current_due_date: Optional[datetime], pattern: str) -> Optional[datetime]:
    """
    Calculates the next due date based on the current due date and recurrence pattern
    """
    if not current_due_date:
        return None
        
    pattern_enum = RecurrencePattern(pattern.lower())
    
    if pattern_enum == RecurrencePattern.DAILY:
        return current_due_date + timedelta(days=1)
    elif pattern_enum == RecurrencePattern.WEEKLY:
        return current_due_date + timedelta(weeks=1)
    elif pattern_enum == RecurrencePattern.MONTHLY:
        # For monthly, we'll add 1 month (approximately 30 days)
        # Note: This is a simplified approach; in production, you'd want to handle month boundaries properly
        return current_due_date + timedelta(days=30)
    elif pattern_enum == RecurrencePattern.YEARLY:
        return current_due_date + timedelta(days=365)
    
    return None

def process_completed_recurring_task(session: Session, task_id: UUID) -> Optional[Task]:
    """
    Process a completed recurring task and create the next occurrence if applicable
    """
    task = session.get(Task, task_id)
    if not task:
        logger.error(f"Task with ID {task_id} not found")
        return None
    
    if not task.is_recurring:
        logger.info(f"Task {task_id} is not recurring, skipping next occurrence creation")
        return None
    
    # Update the original task status to completed
    task.status = "completed"
    session.add(task)
    
    # Create the next occurrence
    next_task = create_next_occurrence(session, task)
    
    session.commit()
    return next_task