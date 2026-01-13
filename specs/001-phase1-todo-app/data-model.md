# Data Model: Phase I - In-Memory Python Console Todo App

**Feature**: Phase I - In-Memory Python Console Todo App
**Date**: 2025-12-12
**Branch**: 001-phase1-todo-app

## Overview
This document defines the data models for the Phase I in-memory Python console todo application.

## Task Entity

### Attributes
- **id**: UUID (required, unique)
  - Auto-generated upon creation
  - Used as primary identifier for operations (update, delete, toggle)
  - Stored as UUID type

- **title**: String (required)
  - Minimum length: 1 character
  - Maximum length: 200 characters
  - Validation: Must not be empty or exceed length limit
  - Used for task identification

- **description**: String (optional, nullable)
  - Maximum length: 500 characters
  - Can be null if not provided
  - Provides additional details about the task

- **completed**: Boolean (required)
  - Default value: False
  - Represents task completion status
  - Can be toggled between True/False

- **created_at**: datetime (required)
  - Auto-generated upon creation
  - Stores timestamp when task was created
  - Used for sorting and tracking

### Validation Rules
1. **Title Length**: Title must be between 1 and 200 characters (inclusive)
2. **Required Fields**: id, title, completed, and created_at are required
3. **ID Uniqueness**: Each task must have a unique UUID
4. **Created Timestamp**: Must be a valid datetime instance

### State Transitions
- **Initial State**: When created, a Task has `completed=False`
- **Completion**: Task state can transition from `completed=False` to `completed=True`
- **Reversion**: Task state can transition from `completed=True` back to `completed=False`

### Relationships
- No relationships with other entities in this implementation

## In-Memory Storage Structure

### Data Container
- **Type**: Python dictionary
- **Key**: UUID (the task.id)
- **Value**: Task object instance

### Operations
- **CREATE**: Add new task to dictionary with UUID as key
- **READ**: Retrieve task using UUID key
- **UPDATE**: Modify task properties by accessing with UUID key
- **DELETE**: Remove task from dictionary using UUID key
- **LIST**: Return all task values from dictionary

## TodoCRUDSubagent Operations

The TodoCRUDSubagent class will implement the following methods:

- `create_task(title: str, description: Optional[str] = None) -> Task`
  - Creates a new task with unique UUID and current timestamp
  - Validates title length requirements
  - Returns the created Task object

- `get_task(task_id: UUID) -> Optional[Task]`
  - Retrieves a task by its UUID
  - Returns None if task doesn't exist

- `get_all_tasks() -> List[Task]`
  - Returns all tasks in storage
  - Can be sorted by creation date or completion status

- `update_task(task_id: UUID, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]`
  - Updates specific task with provided values
  - Validates title length if provided
  - Returns updated Task or None if task doesn't exist

- `delete_task(task_id: UUID) -> bool`
  - Removes task from storage
  - Returns True if successful, False if task doesn't exist

- `toggle_task_status(task_id: UUID) -> Optional[Task]`
  - Changes completed status to the opposite value
  - Returns updated Task or None if task doesn't exist

## TodoService Validation

The TodoService will implement validation before calling the subagent:

- Validate title length (1-200 characters) before creating/updating tasks
- Validate that task exists before updating, deleting, or toggling
- Return appropriate error information if validation fails