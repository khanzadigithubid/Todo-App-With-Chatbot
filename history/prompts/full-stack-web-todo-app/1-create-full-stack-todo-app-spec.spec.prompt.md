---
id: 1
title: Create Full-Stack Todo App Spec
stage: spec
date: 2025-12-15
surface: agent
model: gemini-1.5-pro
feature: full-stack-web-todo-app
branch: 003-full-stack-web-todo-app
user: Khanzadi
command: /sp.specify
labels: [spec, full-stack, web-app]
links:
  spec: specs/003-full-stack-web-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-full-stack-web-todo-app/spec.md
  - specs/003-full-stack-web-todo-app/checklists/requirements.md
tests:
  - none
---

## Prompt

Phase II: Full-Stack Web Todo App with Neon PostgreSQL (Hackathon II) Goal: Transform the Phase I console app into a modern multi-user web application with persistent storage using Neon Serverless PostgreSQL. Authentication (Better Auth) will be added in a later step — exclude it for now. User Stories: - As a user, I can sign up and have my own isolated tasks (tasks linked to user_id). - As a user, I can perform all 5 basic CRUD operations (add, list, update, delete, toggle complete) via a responsive web interface. - As a user, my tasks are saved permanently in the database and survive server restarts. Requirements & Acceptance Criteria: - Monorepo structure with frontend/ (Next.js) and backend/ (FastAPI). - Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS, responsive design (mobile-friendly table, forms, cards). - Backend: FastAPI with SQLModel ORM. - Database: Neon Serverless PostgreSQL (connection via DATABASE_URL env variable). - Database Schema: - users table: id (string PK), email (unique), name, created_at - tasks table: id (int PK), user_id (string FK → users.id), title (str, required), description (text, nullable), completed (bool, default false), created_at, updated_at - Indexes on tasks.user_id and tasks.completed - REST API Endpoints (exact paths as per hackathon): - GET /api/{user_id}/tasks - POST /api/{user_id}/tasks - GET /api/{user_id}/tasks/{id} - PUT /api/{user_id}/tasks/{id} - DELETE /api/{user_id}/tasks/{id} - PATCH /api/{user_id}/tasks/{id}/complete - For this step, user_id will be hardcoded or passed as a query/param in frontend for testing (no JWT/auth yet). - All task operations must filter/create with the correct user_id. - Use Context7 MCP server for latest Next.js 16+, FastAPI, SQLModel, and Neon connection patterns. - UI must be clean and modern (Tailwind cards, hover buttons, responsive grid/table). Output: Generate specs/phase2/spec.md containing: - Project overview for Phase II - Database schema table - API endpoints table - User stories and acceptance criteria - High-level monorepo folder structure - Basic UI description (pages and components needed)

## Response snapshot

Generated the feature specification and quality checklist.

## Outcome

- ✅ Impact: Created the initial specification for the full-stack web todo app.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `specs/003-full-stack-web-todo-app/spec.md`
  - `specs/003-full-stack-web-todo-app/checklists/requirements.md`
  - `history/prompts/full-stack-web-todo-app/1-create-full-stack-todo-app-spec.spec.prompt.md`
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The process of creating the spec was smooth. The user provided a very detailed description which made it easy to generate a comprehensive spec. The script for creating the feature branch failed, but I was able to recover and create the files manually.
