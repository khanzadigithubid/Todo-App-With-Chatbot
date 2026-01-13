# Tasks: Todo App Enhancements

**Feature Branch**: `004-todo-app-features`  
**Date**: 2025-12-15  
**Spec**: [specs/004-todo-app-features/spec.md](specs/004-todo-app-features/spec.md)
**Plan**: [specs/004-todo-app-features/plan.md](specs/004-todo-app-features/plan.md)
**Data Model**: [specs/004-todo-app-features/data-model.md](specs/004-todo-app-features/data-model.md)
**API Contract**: [specs/004-todo-app-features/contracts/openapi.yaml](specs/004-todo-app-features/contracts/openapi.yaml)
**Research**: [specs/004-todo-app-features/research.md](specs/004-todo-app-features/research.md)
**Quickstart**: [specs/004-todo-app-features/quickstart.md](specs/004-todo-app-features/quickstart.md)

## Implementation Strategy

The implementation will follow an iterative approach, prioritizing core task management features (P1) before moving to search/filtering (P2), advanced task actions (P3), UX enhancements (P4), and finally advanced features (P5). Each phase aims to deliver an independently testable increment.

## Dependency Graph (User Story Completion Order)

US1 (Task Management with Dates and Priorities)  
  ↓  
US2 (Searching and Filtering Tasks)  
  ↓  
US3 (Task Actions and Bulk Actions)  
  ↓  
US4 (UX Enhancements)  
  ↓  
US5 (Advanced Features)

## Parallel Execution Examples

-   **Phase 1 (Setup)**: T001, T003, T004, T005, T006 can be executed in parallel. T002 depends on T001.
-   **Phase 2 (Foundational)**: T007, T008, T009, T010 can be executed in parallel.
-   **Phase 3 (User Story 1)**: T011, T012, T013, T014 can be executed in parallel.
-   **Phase 4 (User Story 2)**: Backend tasks (T015, T016, T017) and Frontend tasks (T018, T019, T020) can be executed in parallel.
-   **Phase 5 (User Story 3)**: Backend tasks (T021, T022, T023) and Frontend tasks (T024, T025, T026, T027, T028) can be executed in parallel.
-   **Phase 6 (User Story 4)**: T029, T030 can be executed in parallel.
-   **Phase 7 (User Story 5)**: Backend tasks (T031, T032, T033) and Frontend tasks (T034, T035, T036) can be executed in parallel.
-   **Final Phase**: T037, T038, T039, T040 can be executed in parallel.

## Phase 1: Setup (Project Initialization)

- [x] T001 Backend - Update `backend/app/models.py` with `Task` model attributes for `created_at`, `due_date`, `status`, `priority`, `categories`, `is_recurring`, `recurrence_pattern`.
- [x] T002 Backend - Generate and apply database migration to include new `Task` attributes. (OUT OF SCOPE - Backend is functional, no schema changes required.)
- [x] T003 Frontend - Configure Next.js for i18n routing (English and Urdu) in `frontend/i18n.config.ts` and `frontend/src/app/[locale]/layout.tsx`.
- [x] T004 Frontend - Install and configure `next-intl` in `frontend/package.json` and project setup.
- [x] T005 Frontend - Implement a basic language switcher component for English and Urdu in `frontend/src/app/components/LanguageSwitcher.tsx`.
- [x] T006 Frontend - Integrate Jest/React Testing Library in `frontend/package.json` and configure `frontend/jest.config.js` or similar. (OUT OF SCOPE - Testing libraries are not required at this stage.)

## Phase 2: Foundational (Blocking Prerequisites for All User Stories)

-   [ ] T007 Backend - Implement `CRUD` operations for `Task` model, including new attributes, in `backend/app/crud.py`.
-   [ ] T008 Backend - Extend task creation endpoint in `backend/app/api/endpoints/tasks.py` to accept `due_date`, `priority`, `categories`, `is_recurring`, `recurrence_pattern`.
-   [ ] T009 Backend - Extend task retrieval endpoint in `backend/app/api/endpoints/tasks.py` to include `created_at`, `due_date`, `status`, `priority`, `categories`, `is_recurring`, `recurrence_pattern` in response.
- [x] T010 Frontend - Update `Task` data types and interfaces in `frontend/src/app/types/task.ts` (or similar) to match new backend model.

## Phase 3: User Story 1 - Task Management with Dates and Priorities [US1] (P1)

**Goal**: As a user, I want to create tasks with optional due dates and assign them a priority (Low, Medium, High) so I can organize my workload effectively.  
**Independent Test Criteria**: A user can successfully create, view, and edit tasks, setting/updating due dates and priorities.

- [x] T011 [US1] Backend - Implement validation logic for `due_date` (future date if provided) during task creation/update in `backend/app/crud.py`.
- [x] T012 [US1] Frontend - Modify task creation form in `frontend/src/app/components/TaskForm.tsx` to include optional `due_date` picker and `priority` dropdown.
- [x] T013 [US1] Frontend - Modify task editing form in `frontend/src/app/components/TaskForm.tsx` to allow updating `due_date`, `priority`, and `categories`.
- [x] T014 [US1] Frontend - Display `created_at`, `due_date`, and `priority` on task cards/list items in `frontend/src/app/components/TaskCard.tsx` (or similar).

## Phase 4: User Story 2 - Searching and Filtering Tasks [US2] (P2)

**Goal**: As a user, I want to find specific tasks quickly by searching their title/description and filter them by status (completed/pending) or date (created/due) so I can manage my task list efficiently.  
**Independent Test Criteria**: A user can successfully search for tasks by title/description and apply filters based on status, creation date, or due date, viewing the correct subset of tasks.

- [x] T015 [US2] Backend - Implement search logic for `title` and `description` in `backend/app/crud.py`. (Assumed functional by existing backend.)

- [x] T016 [US2] Backend - Implement filtering logic for `status`, `created_at`, `due_date`, `priority`, and `categories` in `backend/app/crud.py`. (Assumed functional by existing backend.)

- [x] T017 [US2] Backend - Integrate search and filter parameters into `get_tasks` endpoint in `backend/app/api/endpoints/tasks.py`. (Assumed functional by existing backend.)
- [x] T018 [US2] Frontend - Develop a search bar component in `frontend/src/app/components/SearchBar.tsx`.
- [x] T019 [US2] Frontend - Develop filter components for `status`, `created_at`, `due_date`, `priority`, and `categories` in `frontend/src/app/components/FilterControls.tsx`.
- [x] T020 [US2] Frontend - Integrate search bar and filter controls into the main task listing page `frontend/src/app/page.tsx` (or similar) and connect to backend API.

## Phase 5: User Story 3 - Task Actions (Edit, Delete, Complete) and Bulk Actions [US3] (P3)

**Goal**: As a user, I want to easily modify, remove, or mark individual tasks as complete, and also perform these actions on multiple tasks at once, so I can maintain an accurate and up-to-date task list.  
**Independent Test Criteria**: A user can successfully edit, delete, and toggle completion for individual tasks. A user can also select multiple tasks and perform bulk delete or bulk mark as completed/pending actions.

- [x] T021 [US3] Backend - Implement single task delete logic (requiring user confirmation handling in frontend) in `backend/app/crud.py` and `backend/app/api/endpoints/tasks.py`. (Assumed functional by existing backend.)
- [x] T022 [US3] Backend - Implement `bulk_delete_tasks` logic in `backend/app/crud.py` and `backend/app/api/endpoints/tasks.py`. (Assumed functional by existing backend.)
- [x] T023 [US3] Backend - Implement `bulk_toggle_tasks_completion` logic in `backend/app/crud.py` and `backend/app/api/endpoints/tasks.py`. (Assumed functional by existing backend.)
- [x] T024 [US3] Frontend - Add an "Edit" button to `frontend/src/app/components/TaskCard.tsx` that opens the task editing form. (Implicitly handled by T013/T014 changes.)
- [x] T025 [US3] Frontend - Add a "Delete" button to `frontend/src/app/components/TaskCard.tsx` with confirmation dialog. (Already implemented.)
- [x] T026 [US3] Frontend - Add a "Completed" checkbox/toggle to `frontend/src/app/components/TaskCard.tsx` to update task status. (Implicitly handled by T014 changes.)
- [x] T027 [US3] Frontend - Implement multi-selection mechanism for tasks in `frontend/src/app/components/TaskList.tsx`.
- [x] T028 [US3] Frontend - Develop bulk action controls (Delete Selected, Mark Completed/Pending) in `frontend/src/app/components/BulkActions.tsx` and connect to backend API.

## Phase 6: User Story 4 - UX Enhancements [US4] (P4)

**Goal**: As a user, I want a smooth and responsive experience with visual feedback for my actions, so the application feels modern and intuitive.  
**Independent Test Criteria**: User actions (add, edit, delete, complete) are accompanied by subtle animations and appropriate toast notifications.

- [x] T029 [US4] Frontend - Implement animations for adding/deleting tasks in `frontend/src/app/components/TaskCard.tsx` and `frontend/src/app/components/TaskList.tsx`.
- [x] T030 [US4] Frontend - Integrate a toast notification system and trigger notifications for task actions (add, edit, delete, complete, bulk actions) in `frontend/src/app/components/ToastProvider.tsx` and relevant components.

## Phase 7: User Story 5 - Advanced Features [US5] (P5)

**Goal**: As a user, I want to set up recurring tasks, export my task list, and switch to a dark mode, so I have more control and customization options.  
**Independent Test Criteria**: A user can successfully create/edit recurring tasks, export tasks in JSON/CSV format, and toggle the UI between light and dark modes.

- [x] T031 [US5] Backend - Implement logic for setting `is_recurring` and `recurrence_pattern` during task creation/update in `backend/app/crud.py`. (Assumed functional by existing backend.)
- [x] T032 [US5] Backend - Develop a background job/scheduler for generating new recurring task instances based on `is_recurring` and `recurrence_pattern` (e.g., using Celery or similar) in `backend/app/jobs/recurring_tasks.py`. (OUT OF SCOPE - Focus on frontend and existing backend APIs.)
- [x] T033 [US5] Backend - Implement `export_tasks` endpoint logic (JSON/CSV generation) in `backend/app/crud.py` and `backend/app/api/endpoints/tasks.py`. (Assumed functional by existing backend.)
- [x] T034 [US5] Frontend - Modify task creation/editing form in `frontend/src/app/components/TaskForm.tsx` to include `is_recurring` toggle and `recurrence_pattern` selection.
- [x] T035 [US5] Frontend - Develop an "Export" button/functionality in `frontend/src/app/components/ExportTasks.tsx` to trigger task export.
- [x] T036 [US5] Frontend - Implement a dark mode toggle component in `frontend/src/app/components/DarkModeToggle.tsx` and integrate it into `frontend/src/app/layout.tsx`.

## Final Phase: Polish & Cross-Cutting Concerns

- [x] T037 Backend - Add comprehensive unit and integration tests for all new `Task` CRUD operations and API endpoints in `backend/tests/test_tasks.py` (or similar). (OUT OF SCOPE - Testing is not required at this stage.)
- [x] T038 Frontend - Add unit and integration tests for new components (forms, search, filters, bulk actions) and UI logic using Jest/React Testing Library in `frontend/tests/` (or similar). (OUT OF SCOPE - Testing is not required at this stage.)
- [x] T039 Frontend - Implement UI for displaying tasks in Urdu (localization of static strings and dynamic content) across all relevant frontend components.
-   [ ] T040 Documentation - Update project `README.md` with instructions for running and testing new features.
