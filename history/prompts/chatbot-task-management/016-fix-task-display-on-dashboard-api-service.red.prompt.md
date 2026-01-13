---
id: 16
title: "Fix Task Display on Dashboard (API Service)"
stage: red
date_iso: "2025-12-24"
surface: "agent"
model: "gemini"
feature: "chatbot-task-management"
branch: "006-chatbot-task-management"
user: "Khanzadi"
command: "Tasks are being added, but they are not showing on the dashboard UI right now."
labels:
    - "frontend"
    - "backend"
    - "fix"
    - "ui"
    - "dashboard"
    - "api"
links:
    spec: "specs/006-chatbot-task-management/spec.md"
    plan: "specs/006-chatbot-task-management/plan.md"
    tasks: "specs/006-chatbot-task-management/tasks.md"
    ticket: null
    adr: null
    pr: null
files_yaml:
    - "frontend/src/services/api.ts"
tests_yaml: []
outcome: "Fixed the API service functions in the frontend to correctly construct the endpoint URLs with the userId. Instructed the user to restart both servers."
---

## PROMPT

Tasks are being added, but they are not showing on the dashboard UI right now.

## RESPONSE

I have fixed the API service functions in the frontend to correctly fetch and manage tasks. Please restart both your frontend and backend servers, and then check the dashboard at http://localhost:3000/dashboard.
