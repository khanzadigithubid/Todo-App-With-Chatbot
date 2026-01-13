# Feature Specification: Full-Stack Web Todo App

**Feature Branch**: `003-full-stack-web-todo-app`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "Phase II: Full-Stack Web Todo App with Neon PostgreSQL (Hackathon II) Goal: Transform the Phase I console app into a modern multi-user web application with persistent storage using Neon Serverless PostgreSQL. Authentication (Better Auth) will be added in a later step — exclude it for now. User Stories: - As a user, I can sign up and have my own isolated tasks (tasks linked to user_id). - As a user, I can perform all 5 basic CRUD operations (add, list, update, delete, toggle complete) via a responsive web interface. - As a user, my tasks are saved permanently in the database and survive server restarts. Requirements & Acceptance Criteria: - Monorepo structure with frontend/ (Next.js) and backend/ (FastAPI). - Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS, responsive design (mobile-friendly table, forms, cards). - Backend: FastAPI with SQLModel ORM. - Database: Neon Serverless PostgreSQL (connection via DATABASE_URL env variable). - Database Schema: - users table: id (string PK), email (unique), name, created_at - tasks table: id (int PK), user_id (string FK → users.id), title (str, required), description (text, nullable), completed (bool, default false), created_at, updated_at - Indexes on tasks.user_id and tasks.completed - REST API Endpoints (exact paths as per hackathon): - GET /api/{user_id}/tasks - POST /api/{user_id}/tasks - GET /api/{user_id}/tasks/{id} - PUT /api/{user_id}/tasks/{id} - DELETE /api/{user_id}/tasks/{id} - PATCH /api/{user_id}/tasks/{id}/complete - For this step, user_id will be hardcoded or passed as a query/param in frontend for testing (no JWT/auth yet). - All task operations must filter/create with the correct user_id. - Use Context7 MCP server for latest Next.js 16+, FastAPI, SQLModel, and Neon connection patterns. - UI must be clean and modern (Tailwind cards, hover buttons, responsive grid/table). Output: Generate specs/phase2/spec.md containing: - Project overview for Phase II - Database schema table - API endpoints table - User stories and acceptance criteria - High-level monorepo folder structure - Basic UI description (pages and components needed)"

## 1. Overview

This document outlines the plan to transform the existing command-line Todo application into a full-stack, multi-user web application. The new application will feature a modern web interface built with Next.js and a robust backend API powered by FastAPI, with data persisted in a Neon Serverless PostgreSQL database. This phase focuses on core CRUD functionality for tasks, scoped to individual users, laying the groundwork for future enhancements like authentication.

## 2. User Stories & Scenarios

### User Story 1: User Registration (P1)
**As a new user, I want to sign up for the service so that I can have my own private space to manage my tasks.**

**Acceptance Criteria**:
- A user can be created in the database with a unique identifier, email, and name.
- For this phase, user creation may be handled via a simple form or a seed script, as full authentication is out of scope.

### User Story 2: Task Management (P1)
**As a registered user, I want to perform all essential CRUD operations (Create, Read, Update, Delete) on my tasks through a web interface, so that I can manage my to-do list effectively.**

**Acceptance Criteria**:
- **Create**: A user can add a new task with a title and an optional description.
- **Read**: A user can view a list of all their tasks.
- **Update**: A user can edit the title and description of an existing task.
- **Delete**: A user can remove a task from their list.
- **Toggle Complete**: A user can mark a task as complete or incomplete.
- All operations must be associated with the correct `user_id`.

### User Story 3: Data Persistence (P1)
**As a user, I want my tasks to be saved automatically, so that my data is safe and available every time I visit the application.**

**Acceptance Criteria**:
- All created, updated, or deleted tasks are permanently stored in the PostgreSQL database.
- Task state (e.g., `completed` status) persists across sessions and server restarts.

## 3. Requirements

### Functional Requirements

- **FR-001**: The system MUST provide a web-based interface for user and task management.
- **FR-002**: The system MUST associate every task with a specific user.
- **FR-003**: The backend MUST expose RESTful API endpoints for task operations.
- **FR-004**: The system MUST persist all user and task data in a PostgreSQL database.
- **FR-005**: The user interface MUST be responsive and functional on both desktop and mobile devices.
- **FR-006**: For this initial phase, the `user_id` can be hardcoded or passed as a parameter for testing purposes, in lieu of a full authentication system.

### Non-Functional Requirements

- **NFR-001**: The API should respond to requests in under 500ms.
- **NFR-002**: The application should be maintainable and scalable.

## 4. System Architecture

### Monorepo Structure

The project will be organized in a monorepo structure to manage the frontend and backend codebases in a single repository.

```
/
├── backend/         # FastAPI application
│   ├── app/
│   └── ...
├── frontend/        # Next.js application
│   ├── app/
│   └── ...
└── ...
```

### Frontend

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**:
    - `TaskCard`: Displays a single task with controls for editing, deleting, and toggling completion.
    - `TaskList`: Renders a list of `TaskCard` components.
    - `TaskForm`: A form for creating and editing tasks.
    - `MainPage`: The main view containing the `TaskList` and a button to open the `TaskForm`.

### Backend

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Environment**: Connection details will be managed via a `DATABASE_URL` environment variable.

## 5. Data Model

The database will consist of two main tables: `users` and `tasks`.

### `users` Table

| Column      | Type          | Constraints              | Description                  |
|-------------|---------------|--------------------------|------------------------------|
| `id`        | `string`      | **Primary Key**          | Unique identifier for the user |
| `email`     | `string`      | **Unique**, **Not Null** | User's email address         |
| `name`      | `string`      | Not Null                 | User's name                  |
| `created_at`| `datetime`    | Default: `NOW()`         | Timestamp of user creation   |

### `tasks` Table

| Column        | Type          | Constraints                      | Description                           |
|---------------|---------------|----------------------------------|---------------------------------------|
| `id`          | `integer`     | **Primary Key**, Auto-increment  | Unique identifier for the task        |
| `user_id`     | `string`      | **Foreign Key** (-> `users.id`)  | Associates the task with a user       |
| `title`       | `string`      | **Not Null**                     | The title of the task                 |
| `description` | `text`        | Nullable                         | A detailed description of the task    |
| `completed`   | `boolean`     | Default: `false`                 | The completion status of the task     |
| `created_at`  | `datetime`    | Default: `NOW()`                 | Timestamp of task creation            |
| `updated_at`  | `datetime`    | Default: `NOW()`, On Update: `NOW()` | Timestamp of the last task update     |

**Indexes**:
- An index will be created on `tasks.user_id` to optimize queries for a user's tasks.
- An index will be created on `tasks.completed` to optimize filtering by completion status.

## 6. API Endpoints

The backend will expose the following RESTful API endpoints. All endpoints are prefixed with `/api`. For this phase, `{user_id}` will be passed directly.

| Method  | Path                               | Description                      |
|---------|------------------------------------|----------------------------------|
| `GET`   | `/{user_id}/tasks`                 | Get all tasks for a user         |
| `POST`  | `/{user_id}/tasks`                 | Create a new task for a user     |
| `GET`   | `/{user_id}/tasks/{id}`            | Get a single task by ID          |
| `PUT`   | `/{user_id}/tasks/{id}`            | Update a task by ID              |
| `DELETE`| `/{user_id}/tasks/{id}`            | Delete a task by ID              |
| `PATCH` | `/{user_id}/tasks/{id}/complete`   | Mark a task as complete/incomplete |

## 7. Success Criteria

- **SC-001**: A user can successfully create, view, update, and delete tasks through the web interface.
- **SC-002**: All task data is correctly persisted in the database and associated with the correct user.
- **SC-003**: The application is deployed and accessible.
- **SC-004**: The UI is clean, modern, and responsive on mobile and desktop screens.