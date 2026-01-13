# Feature Specification: Phase II: Add Better Auth + JWT Authentication

**Feature Branch**: `005-phase2-auth-jwt`
**Created**: 2025-12-16
**Status**: Draft
**Input**: User description: "Phase II: Add Better Auth + JWT Authentication (Hackathon II) Goal: Complete Phase II by adding full authentication using Better Auth (frontend) and JWT verification (backend). This enables multi-user isolation with persistent tasks in Neon PostgreSQL. Assume previous Phase II core is already implemented: - Monorepo with frontend/ (Next.js 16+ App Router, Tailwind) and backend/ (FastAPI, SQLModel, Neon DB) - Tasks table with user_id foreign key - CRUD endpoints at /api/{user_id}/tasks (currently using hardcoded user_id) New Requirements (Authentication Only): - Implement user signup and signin using Better Auth in Next.js frontend. - Better Auth must issue JWT tokens on login (enable JWT plugin). - Shared secret via environment variable BETTER_AUTH_SECRET (same in frontend and backend). - Frontend API client must attach JWT token in Authorization: Bearer <token> header for every request. - Backend: Add middleware to verify JWT, extract user_id from token payload. - Backend: All task routes must: - Verify JWT token - Extract user_id from token - Match token user_id with {user_id} in URL path - Filter all queries by authenticated user_id - Return 401 Unauthorized if token missing/invalid/expired/mismatched - Users table managed by Better Auth (id, email, name, created_at) - Tasks remain linked to user_id (string, FK to users.id) - After login, frontend redirects to protected tasks page showing only user's tasks. User Flow: 1. User visits /login or /signup 2. Signs up or logs in → Better Auth issues JWT 3. Frontend stores token and attaches to all API calls 4. Backend verifies token → allows access only to own tasks Acceptance Criteria: - Signup creates user in Neon DB (via Better Auth handlers) - Login returns valid JWT - Protected routes reject requests without valid token - Token mismatch (wrong user_id) returns 401 - All existing CRUD operations work per-user Use Context7 MCP server for latest Better Auth docs, PyJWT in FastAPI, and JWT token flow patterns. Output: Generate specs/phase2-auth/spec.md containing: - Authentication flow diagram (text-based) - Better Auth config details - JWT middleware code outline - Updated API behavior (with auth) - Frontend protected routes and token handling - Environment variables required (BETTER_AUTH_SECRET, DATABASE_URL)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Signup and Login (Priority: P1)

A new user can create an account and an existing user can log in to the application.

**Why this priority**: This is the entry point for any user to start using the application and its features.

**Independent Test**: Can be tested by visiting the signup/login page and performing the respective actions. A successful signup will create a user in the database, and a successful login will grant a JWT.

**Acceptance Scenarios**:

1.  **Given** a user is on the signup page, **When** they fill in their details and click "Sign Up", **Then** a new user account is created in the database.
2.  **Given** a user is on the login page, **When** they enter their credentials and click "Log In", **Then** they receive a JWT token and are redirected to their tasks page.

---

### User Story 2 - Accessing Protected Task Routes (Priority: P2)

A logged-in user can access their tasks.

**Why this priority**: This is the core functionality of the application for authenticated users.

**Independent Test**: Can be tested by making API requests to the task endpoints with a valid JWT.

**Acceptance Scenarios**:

1.  **Given** a logged-in user with a valid JWT, **When** they make a request to `/api/{user_id}/tasks`, **Then** they receive a list of their tasks.
2.  **Given** a user without a valid JWT, **When** they make a request to `/api/{user_id}/tasks`, **Then** they receive a 401 Unauthorized error.
3.  **Given** a logged-in user with a valid JWT, **When** they make a request to `/api/{another_user_id}/tasks`, **Then** they receive a 401 Unauthorized error.

---

### Edge Cases

-   What happens when a user tries to access a protected route with an expired token?
-   What happens if the `BETTER_AUTH_SECRET` is different between the frontend and backend?
-   How does the system handle a JWT that is valid but belongs to a user that has been deleted from the database?

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: System MUST allow new users to sign up for an account.
-   **FR-002**: System MUST allow existing users to log in.
-   **FR-003**: System MUST issue a JWT token on successful login.
-   **FR-004**: Frontend MUST store the JWT token and include it in the `Authorization` header for all API requests to protected routes.
-   **FR-005**: Backend MUST have middleware to verify the JWT token on protected routes.
-   **FR-006**: Backend MUST extract the `user_id` from the JWT payload.
-   **FR-007**: Backend MUST ensure that the `user_id` from the token matches the `{user_id}` in the URL path for task-related endpoints.
-   **FR-008**: Backend MUST filter all database queries for tasks by the authenticated `user_id`.
-   **FR-009**: System MUST return a 401 Unauthorized error for missing, invalid, expired, or mismatched JWT tokens.
-   **FR-010**: Frontend MUST redirect users to their protected tasks page after a successful login.

### Key Entities *(include if feature involves data)*

-   **User**: Represents a user of the application. Attributes include `id`, `email`, `name`, `created_at`. Managed by Better Auth.
-   **Task**: Represents a to-do item. Attributes include `id`, `title`, `description`, `completed`, and `user_id` (foreign key to the User entity).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 100% of signup attempts with valid data result in a new user account being created.
-   **SC-002**: 100% of login attempts with valid credentials result in a successful login and JWT issuance.
-   **SC-003**: 100% of API requests to protected routes without a valid JWT are rejected with a 401 Unauthorized error.
-   **SC-004**: A logged-in user can only view, create, edit, and delete their own tasks.
-   **SC-005**: After login, the user is seamlessly redirected to their personal tasks page within 2 seconds.
