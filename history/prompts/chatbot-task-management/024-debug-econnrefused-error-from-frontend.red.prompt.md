---
id: 24
title: "Debug ECONNREFUSED Error from Frontend"
stage: red
date_iso: "2025-12-24"
surface: "agent"
model: "gemini"
feature: "chatbot-task-management"
branch: "006-chatbot-task-management"
user: "Khanzadi"
command: "Failed to proxy http://localhost:8000/api/users/00000000-0000-0000-0000-000000000001/tasks AggregateError: code: 'ECONNREFUSED'"
labels:
    - "frontend"
    - "backend"
    - "fix"
    - "connection"
links:
    spec: "specs/006-chatbot-task-management/spec.md"
    plan: "specs/006-chatbot-task-management/plan.md"
    tasks: "specs/006-chatbot-task-management/tasks.md"
    ticket: null
    adr: null
    pr: null
files_yaml: []
tests_yaml: []
outcome: "Debugging `ECONNREFUSED` error. Asked user to verify backend server is running stably and check console output."
---

## PROMPT

Failed to proxy http://localhost:8000/api/users/00000000-0000-0000-0000-000000000001/tasks AggregateError: code: 'ECONNREFUSED'

## RESPONSE

It seems the frontend is unable to connect to the backend server, resulting in an `ECONNREFUSED` error. This usually means the backend server is not running or is not accessible.

Please ensure your backend server is running without any errors in its console. If it crashed after startup, please provide the full console output from the backend server.

Once you confirm the backend server is running stably, please try accessing the dashboard at `http://localhost:3000/dashboard` again.
