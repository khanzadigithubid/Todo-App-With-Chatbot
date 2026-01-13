# Tasks: Full-Stack Web Todo App

**Input**: Design documents from `/specs/003-full-stack-web-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with `backend` and `frontend` directories.
- [x] T002 [P] Initialize FastAPI backend in `backend/` with `uv`.
- [x] T003 [P] Initialize Next.js frontend in `frontend/` with `npx create-next-app`.
- [x] T004 [P] Configure linting and formatting for backend (e.g., ruff, black).
- [x] T005 [P] Configure linting and formatting for frontend (e.g., ESLint, Prettier).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T006 Setup database connection and session management in `backend/app/database.py`.
- [x] T007 Create base models for `User` and `Task` using SQLModel in `backend/app/models.py`.
- [x] T008 Create Pydantic schemas for API data transfer objects in `backend/app/schemas.py`.
- [x] T009 [P] Setup basic routing in `backend/app/main.py`.

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Allow a new user to be created in the system.

**Independent Test**: A new user can be added to the database via a seed script or a simple form, and the user record is persisted correctly.

### Implementation for User Story 1

- [x] T010 [US1] Implement `create_user` CRUD function in `backend/app/crud.py`.
- [x] T011 [US1] Create an API endpoint to create a user in `backend/app/api/endpoints/users.py`.
- [x] T012 [P] [US1] Create a simple registration form component in `frontend/app/components/RegisterForm.tsx`.
- [x] T013 [US1] Create a page for user registration in `frontend/app/register/page.tsx`.
- [x] T014 [US1] Implement API service call to the create user endpoint in `frontend/app/services/api.ts`.

---

## Phase 4: User Story 2 - Task Management (Priority: P1)

**Goal**: Allow users to perform CRUD operations on their tasks.

**Independent Test**: A user can create, view, update, delete, and toggle the completion status of their tasks through the web interface.

### Implementation for User Story 2

- [x] T015 [US2] Implement CRUD functions for tasks (`create_task`, `get_tasks`, `get_task`, `update_task`, `delete_task`) in `backend/app/crud.py`.
- [x] T016 [US2] Create API endpoints for all task CRUD operations in `backend/app/api/endpoints/tasks.py`.
- [x] T017 [P] [US2] Create `TaskCard` component in `frontend/app/components/TaskCard.tsx`.
- [x] T018 [P] [US2] Create `TaskList` component in `frontend/app/components/TaskList.tsx`.
- [x] T019 [P] [US2] Create `TaskForm` component in `frontend/app/components/TaskForm.tsx`.
- [x] T020 [US2] Create the main page to display the task list and provide controls for adding new tasks in `frontend/app/page.tsx`.
- [x] T021 [US2] Implement API service calls for all task endpoints in `frontend/app/services/api.ts`.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T022 [P] Add basic styling with Tailwind CSS to all frontend components.
- [x] T023 [P] Write a `README.md` with setup and run instructions.
- [x] T024 Code cleanup and refactoring.
- [x] T025 Run quickstart.md validation.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Stories (Phase 3 & 4)**: Depend on Foundational phase completion.
- **Polish (Phase 5)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P1)**: Can start after Foundational (Phase 2).

### Parallel Opportunities

- Most setup tasks can run in parallel.
- Once the foundational phase is complete, work on User Story 1 and User Story 2 can happen in parallel.
- Within each user story, frontend and backend tasks can be parallelized to a large extent. For example, once the API contract is clear, frontend components can be built while the backend endpoints are being implemented.
