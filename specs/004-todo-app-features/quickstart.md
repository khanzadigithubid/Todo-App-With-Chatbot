# Quickstart Guide: Todo App Enhancements

**Feature Branch**: `004-todo-app-features`  
**Date**: 2025-12-15  
**Spec**: [specs/004-todo-app-features/spec.md](specs/004-todo-app-features/spec.md)
**Plan**: [specs/004-todo-app-features/plan.md](specs/004-todo-app-features/plan.md)
**API Contract**: [specs/004-todo-app-features/contracts/openapi.yaml](specs/004-todo-app-features/contracts/openapi.yaml)

This guide provides instructions to quickly get started with the enhanced Todo application, focusing on the new features.

## 1. Environment Setup

Refer to the main `README.md` in the project root for detailed instructions on setting up the development environment, including Python (uv), Node.js, and other prerequisites.

## 2. Running the Application

Once the environment is set up:

1.  **Start the Backend**:
    Navigate to the `backend/` directory and follow the instructions in its `README.md` or main project `README.md` to start the FastAPI server.
    *(Example: `uvicorn app.main:app --reload`)*

2.  **Start the Frontend**:
    Navigate to the `frontend/` directory and follow the instructions in its `README.md` or main project `README.md` to start the Next.js application.
    *(Example: `npm run dev`)*

## 3. Interacting with New Features (API Examples)

The enhanced features are exposed via the backend API. Refer to the [API Contract (OpenAPI specification)](specs/004-todo-app-features/contracts/openapi.yaml) for full details on endpoints, request/response formats, and available parameters.

Here are high-level examples of how to interact with the new functionalities. Assume the API is running at `http://localhost:8000/api/v1`.

### A. Create a Task with Due Date, Priority, and Categories

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Buy groceries",
           "description": "Milk, eggs, bread, and fruits",
           "due_date": "2025-12-20T18:00:00Z",
           "priority": "high",
           "categories": ["Personal", "Shopping"],
           "is_recurring": false
         }'
```

### B. Get Tasks with Search and Filters

```bash
# Get all tasks
curl -X GET "http://localhost:8000/api/v1/tasks"

# Search tasks by title/description
curl -X GET "http://localhost:8000/api/v1/tasks?search=milk"

# Filter tasks by status and priority
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending&priority=high"

# Filter tasks due before a specific date
curl -X GET "http://localhost:8000/api/v1/tasks?due_before=2025-12-31T23:59:59Z"
```

### C. Update a Task

```bash
# Assuming task_id is 'your-task-uuid'
curl -X PUT "http://localhost:8000/api/v1/tasks/your-task-uuid" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Buy groceries and make dinner",
           "status": "completed",
           "priority": "medium"
         }'
```

### D. Delete a Task

```bash
# Assuming task_id is 'your-task-uuid'
curl -X DELETE "http://localhost:8000/api/v1/tasks/your-task-uuid"
```

### E. Toggle Task Completion

```bash
# Assuming task_id is 'your-task-uuid'
curl -X PATCH "http://localhost:8000/api/v1/tasks/your-task-uuid/toggle-complete"
```

### F. Bulk Delete Tasks

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/bulk-delete" \
     -H "Content-Type: application/json" \
     -d '{
           "task_ids": ["uuid-task-1", "uuid-task-2"]
         }'
```

### G. Bulk Mark Tasks as Completed

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/bulk-toggle-complete" \
     -H "Content-Type: application/json" \
     -d '{
           "task_ids": ["uuid-task-3", "uuid-task-4"],
           "status": "completed"
         }'
```

### H. Export Tasks

```bash
# Export tasks as JSON
curl -X GET "http://localhost:8000/api/v1/tasks/export?format=json"

# Export tasks as CSV
curl -X GET "http://localhost:8000/api/v1/tasks/export?format=csv"
```
