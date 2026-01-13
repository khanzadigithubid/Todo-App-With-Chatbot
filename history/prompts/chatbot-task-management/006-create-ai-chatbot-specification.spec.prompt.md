---
id: 6
title: "Create AI Chatbot Specification"
stage: spec
date_iso: "2025-12-24"
surface: "agent"
model: "gemini"
feature: "chatbot-task-management"
branch: "006-chatbot-task-management"
user: "Khanzadi"
command: "/sp.specify"
labels:
    - "ai"
    - "chatbot"
    - "specification"
links:
    spec: "specs/006-chatbot-task-management/spec.md"
    ticket: null
    adr: null
    pr: null
files_yaml:
    - "specs/006-chatbot-task-management/spec.md"
    - "specs/006-chatbot-task-management/checklists/requirements.md"
tests_yaml: []
---

## PROMPT

/sp.specify Phase III: AI Chatbot for Task Management with OpenAI Agents SDK (Hackathon II) Goal: Build a conversational chatbot that performs all 5 basic task operations (add, list, update, delete, complete) via natural language. Use OpenAI Agents SDK for agent logic. Integrate with the existing Phase 2 Neon DB for real task storage. Remove authentication/JWT from the chat endpoint for easy testing. Use plain Next.js UI with tailwind. Assume Phase 2 is complete: - Monorepo with frontend/ (Next.js 16+ App Router, Tailwind) - Backend (FastAPI, SQLModel, Neon DB, CRUD endpoints at /api/{user_id}/tasks) New Requirements (Chatbot with Tools): - Backend: Add POST /api/chat endpoint - Request: {"message": str} - Response: {"response": str, "tool_calls": array if any} - Use OpenAI Agents SDK (Agent + Runner) with gpt-4o model. - Add 5 custom tools to the agent: - add_task: params (title: str required, description: str optional); adds to Neon DB tasks table (hardcode user_id="testuser" for now) - list_tasks: params (status: str optional "all/pending/completed"); queries Neon DB (hardcode user_id="testuser") - complete_task: params (task_id: int); toggles completed in DB - delete_task: params (task_id: int); deletes from DB - update_task: params (task_id: int, title: str optional, description: str optional); updates in DB - Tools use SQLModel + Neon DB (DATABASE_URL env) – filter by hardcoded user_id="testuser". - Update /api/chat: Run agent with tools; agent calls tools based on message; return response + tool results. - Frontend: Add /chat page in Next.js: - Message list (user/assistant bubbles) - Input field + send button - Call /api/chat on send - Display responses and tool results (e.g., "Task added: Buy milk") - Use Context7 MCP server for latest OpenAI Agents SDK tool integration. Testing Steps (Agent must auto-test these): 1. Run backend (uvicorn main:app --reload) 2. Test endpoint with curl: curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message": "Add a task to buy milk"}' Expected: Response mentions task added (check Neon DB manually) 3. Test list: curl -d '{"message": "List all tasks"}' http://localhost:8000/api/chat 4. Frontend /chat page: Open in browser, send messages – see if DB updates. 5. Verify tools work on real Neon DB (same as Phase 2 UI). Natural Language Examples: - "Add a task to buy milk" → Calls add_task → "Task added: Buy milk" - "List all tasks" → Calls list_tasks → Lists tasks from DB Acceptance Criteria: - Chatbot performs real DB operations via tools - Agent handles intent correctly Output: Generate specs/phase3-chatbot-noauth/spec.md with: - Tools table (params, returns, examples) - Chat endpoint format - Testing commands (curl examples) - Frontend chat page description - Example conversations

## RESPONSE

I have created the feature specification and the associated quality checklist. All validation checks have passed.

The new feature specification is located at: `specs/006-chatbot-task-management/spec.md`

I have created and switched to the new feature branch: `006-chatbot-task-management`.
