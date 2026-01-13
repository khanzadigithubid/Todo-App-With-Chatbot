from typing import Dict, List, Optional
from .models import Task
from uuid import uuid4


class InMemoryStorage:
    """
    In-memory storage using Python dictionaries to store tasks.
    """
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def add_task(self, task: Task) -> Task:
        """Add a task to storage."""
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        return list(self._tasks.values())

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update a task by ID with provided attributes."""
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False


class TodoCRUDSubagent:
    """
    Reusable TodoCRUDSubagent class that encapsulates all task management functionality.
    This class will be imported in Phase II–V.
    """
    def __init__(self, storage=None):
        # Import PostgresStorage here to avoid circular imports
        from .postgres_storage import PostgresStorage

        # Use PostgreSQL storage by default, with in-memory as fallback
        if storage is None:
            try:
                self.storage = PostgresStorage()
            except Exception as e:
                print(f"Failed to connect to PostgreSQL: {e}. Falling back to in-memory storage.")
                self.storage = InMemoryStorage()
        else:
            self.storage = storage
    
    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Creates a new task with unique UUID and current timestamp.
        Validates title length requirements.
        Returns the created Task object.
        """
        from uuid import uuid4
        from datetime import datetime
        
        # Create a new task with a unique ID
        task = Task(
            id=str(uuid4()),
            title=title,
            description=description,
            status="pending",
            created_at=datetime.now()
        )
        return self.storage.add_task(task)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieves a task by its UUID.
        Returns None if task doesn't exist.
        """
        return self.storage.get_task(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Returns all tasks in storage.
        Can be sorted by creation date or completion status.
        """
        return self.storage.get_all_tasks()
    
    def update_task(self, task_id: str, title: Optional[str] = None,
                    description: Optional[str] = None, status: Optional[str] = None) -> Optional[Task]:
        """
        Updates specific task with provided values.
        Validates title length if provided.
        Returns updated Task or None if task doesn't exist.
        """
        if title is not None and (len(title) < 1 or len(title) > 200):
            raise ValueError("Title must be between 1 and 200 characters")

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if status is not None:
            update_data['status'] = status

        return self.storage.update_task(task_id, **update_data)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Removes task from storage.
        Returns True if successful, False if task doesn't exist.
        """
        return self.storage.delete_task(task_id)
    
    def toggle_task_status(self, task_id: str) -> Optional[Task]:
        """
        Changes status to the opposite value.
        Returns updated Task or None if task doesn't exist.
        """
        task = self.storage.get_task(task_id)
        if task:
            task.status = "completed" if task.status == "pending" else "pending"
            return self.storage.update_task(task_id, status=task.status)
        return None