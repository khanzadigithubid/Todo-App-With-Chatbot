# User Stories: Phase I - In-Memory Python Console Todo App

## Overview
This document details the user stories for the Phase I console todo application that will be used as reference during implementation.

## User Stories Table

| ID | User Story | Priority | Acceptance Criteria | Status |
|----|------------|----------|-------------------|--------|
| US-001 | As a busy user, I want to quickly add a task with title & optional description so I don't forget anything | P1 | Task can be added with title and optional description, assigned UUID, and stored with creation timestamp | Pending |
| US-002 | As a user, I want to see all my tasks in a beautiful colored table so I know what's pending | P1 | All tasks displayed in rich, colored table with emojis (✓ for done, ○ for pending), borders, and distinct colors for status | Pending |
| US-003 | As a user, I want to update a task by ID when plans change | P2 | Task details can be modified by specifying the task ID; system validates input and displays appropriate feedback | Pending |
| US-004 | As a user, I want to delete a task that's no longer needed | P2 | Task can be removed by specifying the task ID; system validates ID and confirms deletion | Pending |
| US-005 | As a user, I want to mark a task complete/incomplete to feel productive | P3 | Task completion status can be toggled by specifying the task ID; change reflects immediately in task list | Pending |

## Bonus Requirements

| ID | Bonus Requirement | Status |
|----|------------------|--------|
| BR-001 | Create a reusable TodoCRUDSubagent class that will be imported in Phase II–V | Pending |
| BR-002 | Add Urdu prompts & success messages (e.g., "Task ban gaya!", "Title daaliye:") | Pending |
| BR-003 | Zero manual code — everything from Claude | Pending |

## Acceptance Criteria Checklist

- [ ] Runs with: uv run main.py
- [ ] Uses only UV + rich + typer
- [ ] Rich table with emojis (Done / Pending), colors, borders
- [ ] Task model has: id (UUID), title, description (optional), completed, created_at
- [ ] Input validation (title 1–200 chars)
- [ ] Graceful error handling (invalid ID → red message)
- [ ] Zero manual code — everything from Claude
- [ ] Generated specs/phase1/spec.md + specs/phase1/user-stories.md with clear tables that judges can tick

## Validation Scenarios

### Add Task
- Given: User wants to add a new task
- When: User enters a title (1-200 characters) and optional description
- Then: System creates a new task with UUID, timestamp, and pending status

### View Tasks
- Given: User has multiple tasks in the system
- When: User requests to view all tasks
- Then: System displays all tasks in a rich, colored table with appropriate visual indicators

### Update Task
- Given: User has existing tasks
- When: User specifies a valid task ID and new details
- Then: System updates the task and confirms the change

### Delete Task
- Given: User wants to remove a task
- When: User specifies a valid task ID
- Then: System removes the task and confirms deletion

### Mark Complete/Incomplete
- Given: User has tasks with various statuses
- When: User specifies a valid task ID and desired status
- Then: System updates the task's completion status and reflects the change in the display

## Edge Cases to Handle

- Invalid task IDs during update/delete operations
- Title length validation (1-200 characters)
- Non-existent tasks when trying to mark complete/incomplete
- Empty task list display
- Invalid input types for task IDs