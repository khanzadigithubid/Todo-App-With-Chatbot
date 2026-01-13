# TodoCRUDSubagent Documentation

The `TodoCRUDSubagent` class is a reusable component designed for task management operations. This class will be imported and used in Phase II–V of the Hackathon II project.

## Purpose

The TodoCRUDSubagent encapsulates all task management functionality, providing a consistent interface for:
- Creating tasks
- Reading tasks (individual and all)
- Updating tasks
- Deleting tasks
- Toggling task completion status

## Usage

The TodoCRUDSubagent can be instantiated and used as follows:

```python
from src.todo.storage import TodoCRUDSubagent

# Create an instance
subagent = TodoCRUDSubagent()

# Create a new task
task = subagent.create_task("New task", "Task description")

# Get a specific task
retrieved_task = subagent.get_task(task.id)

# Get all tasks
all_tasks = subagent.get_all_tasks()

# Update a task
updated_task = subagent.update_task(task.id, title="Updated title", description="Updated description")

# Toggle task status
toggled_task = subagent.toggle_task_status(task.id)

# Delete a task
success = subagent.delete_task(task.id)
```

## Interface

### Methods

- `create_task(title: str, description: Optional[str] = None) -> Task`
  - Creates a new task with unique UUID and current timestamp
  - Requires title (1-200 characters)
  - Description is optional

- `get_task(task_id: str) -> Optional[Task]`
  - Retrieves a task by its UUID
  - Returns None if task doesn't exist

- `get_all_tasks() -> List[Task]`
  - Returns all tasks in storage

- `update_task(task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]`
  - Updates specific task with provided values
  - Validates title length if provided
  - Returns updated Task or None if task doesn't exist

- `delete_task(task_id: str) -> bool`
  - Removes task from storage
  - Returns True if successful, False if task doesn't exist

- `toggle_task_status(task_id: str) -> Optional[Task]`
  - Changes completed status to the opposite value
  - Returns updated Task or None if task doesn't exist

## Dependencies

- Python 3.13+
- src.todo.models.Task dataclass
- In-memory storage (no external DB dependencies)

## Design Principles

- **Reusability**: Designed to be imported and used across multiple phases
- **Encapsulation**: All CRUD operations contained within a single class
- **Consistency**: Uniform interface for task operations
- **Validation**: Built-in validation for data integrity