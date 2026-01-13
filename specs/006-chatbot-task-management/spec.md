# Feature Specification: AI Chatbot for Task Management

**Version**: 1.0
**Status**: In Progress
**Author**: Gemini
**Last Updated**: 2025-12-24

## 1. Introduction

This document outlines the feature specification for an AI-powered conversational chatbot for task management. The chatbot will integrate with the existing Neon DB and leverage the OpenAI Agents SDK to perform basic task operations (add, list, update, delete, complete) through a natural language interface. This feature is part of Phase III of the project and is designed for rapid implementation and testing without authentication.

## 2. Problem Statement

Users need a more intuitive and faster way to manage their tasks without navigating through a UI. A conversational interface allows users to perform CRUD (Create, Read, Update, Delete) operations on their tasks using natural language, improving efficiency and user experience.

## 3. Goals and Objectives

### 3.1. Goals

- Provide a conversational interface for task management.
- Integrate with the existing backend and database to ensure data consistency.
- Utilize a powerful AI agent to understand and execute user commands accurately.

### 3.2. Objectives

- Implement a new API endpoint (`/api/chat`) to handle chat messages.
- Create an AI agent using the OpenAI Agents SDK with `gpt-4o`.
- Develop five custom tools for the agent to interact with the database.
- Build a simple, clean frontend chat interface using Next.js and Tailwind CSS.
- Ensure the chatbot can perform all five basic task operations on the Neon DB.

## 4. Functional Requirements

### 4.1. Backend

- **FR1: Chat Endpoint**: The system MUST expose a `POST /api/chat` endpoint.
  - **FR1.1**: The endpoint MUST accept a JSON payload with a `"message"` field (string).
  - **FR1.2**: The endpoint MUST return a JSON payload with a `"response"` field (string) and an optional `"tool_calls"` array.
  - **FR1.3**: The endpoint MUST NOT require JWT authentication for testing purposes.

- **FR2: AI Agent**: The backend MUST use the OpenAI Agents SDK to create an agent.
  - **FR2.1**: The agent MUST use the `gpt-4o` model.
  - **FR2.2**: The agent MUST be configured with five custom tools for task management.

- **FR3: Custom Tools**: The following tools MUST be created and integrated with the agent:
  - **FR3.1: `add_task`**:
    - **Parameters**: `title` (string, required), `description` (string, optional).
    - **Action**: Adds a new task to the Neon DB `tasks` table.
    - **Note**: A hardcoded `user_id` of `"testuser"` will be used.
  - **FR3.2: `list_tasks`**:
    - **Parameters**: `status` (string, optional, values: "all", "pending", "completed").
    - **Action**: Queries and returns tasks from the Neon DB for `"testuser"`.
  - **FR3.3: `complete_task`**:
    - **Parameters**: `task_id` (integer, required).
    - **Action**: Toggles the `completed` status of a task in the DB.
  - **FR3.4: `delete_task`**:
    - **Parameters**: `task_id` (integer, required).
    - **Action**: Deletes a task from the DB.
  - **FR3.5: `update_task`**:
    - **Parameters**: `task_id` (integer, required), `title` (string, optional), `description` (string, optional).
    - **Action**: Updates a task's details in the DB.

### 4.2. Frontend

- **FR4: Chat Page**: A new page MUST be created at `/chat`.
  - **FR4.1**: The page MUST display a list of messages as user and assistant bubbles.
  - **FR4.2**: The page MUST include a text input field and a "Send" button.
  - **FR4.3**: On "Send", the frontend MUST make a `POST` request to the `/api/chat` endpoint.
  - **FR4.4**: The frontend MUST display the assistant's response and any tool call results.

## 5. Non-Functional Requirements

- **NFR1: Performance**: The chatbot response time should be near real-time, dependent on the OpenAI API latency.
- **NFR2: Usability**: The chat interface should be simple, intuitive, and easy to use.
- **NFR3: Scalability**: The backend should be able to handle a reasonable number of concurrent chat sessions.

## 6. Assumptions and Dependencies

- **A1**: Phase 2 of the project is complete and functional.
- **A2**: The Neon DB is accessible via the `DATABASE_URL` environment variable.
- **A3**: The OpenAI Agents SDK is available and compatible with the existing environment.
- **D1**: This feature depends on the OpenAI API for agent logic.

## 7. User Scenarios

- **Scenario 1: Adding a Task**
  - **User**: Types "Add a new task: buy groceries" and clicks Send.
  - **System**: Calls the `add_task` tool and responds with "Task 'buy groceries' has been added."

- **Scenario 2: Listing Tasks**
  - **User**: Types "Show me all my pending tasks".
  - **System**: Calls the `list_tasks` tool with `status="pending"` and displays the list of tasks.

- **Scenario 3: Completing a Task**
  - **User**: Types "Complete task number 123".
  - **System**: Calls the `complete_task` tool for `task_id=123` and responds with "Task 123 has been marked as complete."

## 8. Testing

### 8.1. Backend Testing

- **T1**: Start the backend server: `uvicorn main:app --reload`.
- **T2**: Test the `add_task` tool via `curl`:
  ```bash
  curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message": "Add a task to buy milk"}'
  ```
  - **Expected**: The response indicates the task was added. Manually verify in the Neon DB.
- **T3**: Test the `list_tasks` tool via `curl`:
  ```bash
  curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message": "List all tasks"}'
  ```
  - **Expected**: The response contains a list of tasks from the database.

### 8.2. Frontend Testing

- **T4**: Navigate to the `/chat` page in a web browser.
- **T5**: Send various natural language commands to add, list, update, complete, and delete tasks.
- **T6**: Verify that the UI updates correctly and the changes are reflected in the Neon DB.

## 9. Example Conversations

- **User**: "add task buy milk description whole milk"
- **Assistant**: "Okay, I've added the task 'buy milk' with the description 'whole milk'." (Calls `add_task`)

- **User**: "what are my tasks"
- **Assistant**: "You have 3 tasks: 1. buy milk (pending), 2. walk the dog (pending), 3. pay bills (completed)." (Calls `list_tasks`)

- **User**: "delete task 2"
- **Assistant**: "I have deleted the task 'walk the dog'." (Calls `delete_task`)
