# Tasks for Feature: Phase II: Add Better Auth + JWT Authentication

This file outlines the tasks required to implement the feature.

## Phase 1: Setup

- [x] T001 Install backend dependencies using `uv pip install -r requirements.txt` in the `backend` directory.
- [x] T002 Install frontend dependencies using `npm install` in the `frontend` directory.
- [x] T003 Configure backend environment variables in `backend/.env`.
- [x] T004 Configure frontend environment variables in `frontend/.env.local`.

## Phase 2: Foundational

- [x] T005 [P] Create JWT authentication middleware in `backend/app/middleware.py`.
- [x] T006 Integrate the JWT middleware into the FastAPI application in `backend/app/main.py`.

## Phase 3: User Story 1 - User Signup and Login

- [x] T007 [US1] Create signup and login pages in the frontend using Better Auth components in `frontend/src/app/(auth)/`.
- [x] T008 [US1] Implement the logic to store the JWT in the frontend upon successful login in `frontend/src/services/authService.ts`.
- [x] T009 [US1] Implement the logic to redirect the user to the tasks page after login in `frontend/src/app/(auth)/login/page.tsx`.

## Phase 4: User Story 2 - Accessing Protected Task Routes

- [x] T010 [US2] Apply the JWT middleware to the task-related API endpoints in `backend/app/main.py`.
- [x] T011 [US2] Modify the task-related CRUD functions in `backend/app/crud.py` to filter tasks by the authenticated user's ID.
- [x] T012 [US2] Update the frontend API client in `frontend/src/services/taskService.ts` to include the JWT in the `Authorization` header for all requests to task-related endpoints.

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T013 Review and refactor code for clarity, performance, and adherence to coding standards.
- [x] T014 Update `README.md` with instructions on how to use the new authentication feature.

## Dependencies

- User Story 2 is dependent on the completion of User Story 1.

## Parallel Execution

- Tasks marked with `[P]` can be executed in parallel.
- Within each user story, frontend and backend tasks can be worked on in parallel to some extent. For example, while the backend middleware is being developed, the frontend login pages can be created.

## Implementation Strategy

The implementation will follow a phased approach, starting with the foundational setup and then implementing each user story incrementally. This allows for early testing and validation of each part of the feature. The MVP (Minimum Viable Product) will be the completion of User Story 1, which will provide the core authentication functionality.
