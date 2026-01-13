---
id: 23
title: "Fix Foreign Key Violation on Task Creation"
stage: red
date_iso: "2025-12-24"
surface: "agent"
model: "gemini"
feature: "chatbot-task-management"
branch: "006-chatbot-task-management"
user: "Khanzadi"
command: "ERROR:root:Error creating task: (psycopg2.errors.ForeignKeyViolation) insert or update on table \"task\" violates foreign key constraint \"task_user_id_fkey\"
DETAIL: Key (user_id)=(00000000-0000-0000-0000-000000000001) is not present in table \"user\""."
labels:
    - "backend"
    - "fix"
    - "database"
    - "foreign-key"
links:
    spec: "specs/006-chatbot-task-management/spec.md"
    plan: "specs/006-chatbot-task-management/plan.md"
    tasks: "specs/006-chatbot-task-management/tasks.md"
    ticket: null
    adr: null
    pr: null
files_yaml:
    - "backend/app/main.py"
tests_yaml: []
outcome: "Fixed a `psycopg2.errors.ForeignKeyViolation` by ensuring the hardcoded user is created at application startup. Instructed the user to restart the backend server."
---

## PROMPT

ERROR:root:Error creating task: (psycopg2.errors.ForeignKeyViolation) insert or update on table "task" violates foreign key constraint "task_user_id_fkey"
DETAIL:  Key (user_id)=(00000000-0000-0000-0000-000000000001) is not present in table "user".

## RESPONSE

I have fixed the issue where the hardcoded user was not being created on startup, which caused the foreign key violation. Please restart your backend server for the changes to take effect.
