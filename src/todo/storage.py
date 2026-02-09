# src/todo/storage.py

from .models import Task, Priority
from typing import List, Optional
from datetime import datetime

class InMemoryStorage:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def create_task(self, title: str, description: Optional[str] = None, 
                   priority: str = "medium") -> Task:
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=Priority[priority.upper()]
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None, completed: Optional[bool] = None,
                   priority: Optional[str] = None) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed
            if priority is not None:
                task.priority = Priority[priority.upper()]
            task.updated_at = datetime.now()
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            task.updated_at = datetime.now()
            return task
        return None

# Global instance of storage
storage = InMemoryStorage()