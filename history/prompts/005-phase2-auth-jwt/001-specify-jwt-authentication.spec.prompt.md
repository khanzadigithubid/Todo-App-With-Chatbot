---
id: 001
title: Specify JWT Authentication
stage: spec
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 005-phase2-auth-jwt
branch: 005-phase2-auth-jwt
user: unknown
command: /sp.specify
labels: [auth, jwt, phase2]
links:
  spec: specs/005-phase2-auth-jwt/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-phase2-auth-jwt/spec.md
  - specs/005-phase2-auth-jwt/checklists/requirements.md
tests:
  - none
---

## Prompt

Phase II: Add Better Auth + JWT Authentication (Hackathon II) Goal: Complete Phase II by adding full authentication using Better Auth (frontend) and JWT verification (backend). This enables multi-user isolation with persistent tasks in Neon PostgreSQL. Assume previous Phase II core is already implemented: - Monorepo with frontend/ (Next.js 16+ App Router, Tailwind) and backend/ (FastAPI, SQLModel, Neon DB) - Tasks table with user_id foreign key - CRUD endpoints at /api/{user_id}/tasks (currently using hardcoded user_id) New Requirements (Authentication Only): - Implement user signup and signin using Better Auth in Next.js frontend. - Better Auth must issue JWT tokens on login (enable JWT plugin). - Shared secret via environment variable BETTER_AUTH_SECRET (same in frontend and backend). - Frontend API client must attach JWT token in Authorization: Bearer <token> header for every request. - Backend: Add middleware to verify JWT, extract user_id from token payload. - Backend: All task routes must: - Verify JWT token - Extract user_id from token - Match token user_id with {user_id} in URL path - Filter all queries by authenticated user_id - Return 401 Unauthorized if token missing/invalid/expired/mismatched - Users table managed by Better Auth (id, email, name, created_at) - Tasks remain linked to user_id (string, FK to users.id) - After login, frontend redirects to protected tasks page showing only user's tasks. User Flow: 1. User visits /login or /signup 2. Signs up or logs in → Better Auth issues JWT 3. Frontend stores token and attaches to all API calls 4. Backend verifies token → allows access only to own tasks Acceptance Criteria: - Signup creates user in Neon DB (via Better Auth handlers) - Login returns valid JWT - Protected routes reject requests without valid token - Token mismatch (wrong user_id) returns 401 - All existing CRUD operations work per-user Use Context7 MCP server for latest Better Auth docs, PyJWT in FastAPI, and JWT token flow patterns. Output: Generate specs/phase2-auth/spec.md containing: - Authentication flow diagram (text-based) - Better Auth config details - JWT middleware code outline - Updated API behavior (with auth) - Frontend protected routes and token handling - Environment variables required (BETTER_AUTH_SECRET, DATABASE_URL)

## Response snapshot

Created a new feature branch `005-phase2-auth-jwt`, and generated the specification file `specs/005-phase2-auth-jwt/spec.md` and a corresponding quality checklist.

## Outcome

- ✅ Impact: Successfully created the feature specification.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `specs/005-phase2-auth-jwt/spec.md`
  - `specs/005-phase2-auth-jwt/checklists/requirements.md`
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The initial attempt to use the script failed, but I was able to recover by creating the files and branch manually.
