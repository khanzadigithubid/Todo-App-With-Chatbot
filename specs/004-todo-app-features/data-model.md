# Data Model: Todo App Enhancements

**Feature Branch**: `004-todo-app-features`  
**Date**: 2025-12-15  
**Spec**: [specs/004-todo-app-features/spec.md](specs/004-todo-app-features/spec.md)
**Plan**: [specs/004-todo-app-features/plan.md](specs/004-todo-app-features/plan.md)

## Entities

### Task

Represents a single to-do item in the application.

**Attributes**:

-   `id`:
    -   **Type**: String (UUID)
    -   **Description**: Unique identifier for the task.
    -   **Validation**: Mandatory, unique.
-   `title`:
    -   **Type**: String
    -   **Description**: Main description/name of the task.
    -   **Validation**: Mandatory, minimum length 1 character, maximum length (e.g., 255 characters).
-   `description`:
    -   **Type**: String
    -   **Description**: Optional detailed description of the task.
    -   **Validation**: Optional.
-   `created_at`:
    -   **Type**: Datetime
    -   **Description**: Timestamp when the task was created.
    -   **Validation**: Mandatory, auto-generated on creation.
-   `due_date`:
    -   **Type**: Datetime
    -   **Description**: Optional target completion date for the task.
    -   **Validation**: Optional, must be a future date if provided (unless explicitly allowed for past dates by business logic).
-   `status`:
    -   **Type**: Enum (`pending`, `completed`)
    -   **Description**: Current state of the task.
    -   **Validation**: Mandatory, default `pending`.
    -   **State Transitions**: `pending` <-> `completed`.
-   `priority`:
    -   **Type**: Enum (`low`, `medium`, `high`)
    -   **Description**: Importance level of the task.
    -   **Validation**: Mandatory, default `medium`.
-   `categories`:
    -   **Type**: List of Strings
    -   **Description**: Tags or categories associated with the task (e.g., "Work", "Personal").
    -   **Validation**: Optional, each string in the list must adhere to length/character constraints.
-   `is_recurring`:
    -   **Type**: Boolean
    -   **Description**: Indicates if the task is a recurring one.
    -   **Validation**: Optional, default `false`.
-   `recurrence_pattern`:
    -   **Type**: Enum (`daily`, `weekly`, `monthly`)
    -   **Description**: Pattern for recurring tasks (only applicable if `is_recurring` is `true`).
    -   **Validation**: Optional, mandatory if `is_recurring` is `true`.

## Relationships

-   **Task** has a **one-to-many** relationship with (implicit) **Task Instances** for recurring tasks (each recurrence creates a new task instance).
-   No explicit relationships with other entities defined in this feature spec.
