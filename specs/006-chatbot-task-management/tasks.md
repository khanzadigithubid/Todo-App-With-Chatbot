# Tasks: AI Chatbot for Task Management

**Feature**: `006-chatbot-task-management`
**Spec**: `specs/006-chatbot-task-management/spec.md`

This document outlines the tasks required to implement the AI Chatbot for Task Management feature.

## Phase 1: Setup

- [X] T001 Install OpenAI Python library: `uv pip install openai`
- [X] T002 Add `OPENAI_API_KEY` to your environment variables.

## Phase 2: Foundational (Backend)

- [X] T003 [P] Create `backend/app/tools/task_tools.py` with placeholder functions for `add_task`, `list_tasks`, `complete_task`, `delete_task`, and `update_task`.
- [X] T004 Create `backend/app/api/endpoints/chat.py` with a basic FastAPI router and a `POST /` endpoint for the chat functionality.
- [X] T005 [P] In `backend/app/main.py`, include the new `chat` router with the prefix `/api/chat`.

## Phase 3: User Story 1 - Add Task

- **Goal**: Users can add a new task via the chatbot.
- **Independent Test Criteria**: A user can send a message like "Add a task to buy milk", and the task will be created in the database.

- [X] T006 [US1] Implement the `add_task` function in `backend/app/tools/task_tools.py` to create a new task in the database.
- [X] T007 [US1] In `backend/app/api/endpoints/chat.py`, create an OpenAI agent and pass the `add_task` tool to it.
- [X] T008 [US1] Implement the logic in the chat endpoint to call the agent and return the response.
- [X] T009 [US1] Create a test in `backend/tests/test_chat.py` to verify that the `add_task` tool works correctly.

## Phase 4: User Story 2 - List Tasks

- **Goal**: Users can list their tasks via the chatbot.
- **Independent Test Criteria**: A user can send a message like "List all my tasks", and the chatbot will return a list of tasks from the database.

- [X] T010 [US2] Implement the `list_tasks` function in `backend/app/tools/task_tools.py`.
- [X] T011 [US2] Add the `list_tasks` tool to the agent in `backend/app/api/endpoints/chat.py`.
- [X] T012 [US2] Create a test in `backend/tests/test_chat.py` to verify that the `list_tasks` tool works correctly.

## Phase 5: User Story 3 - Complete Task

- **Goal**: Users can mark a task as complete via the chatbot.
- **Independent Test Criteria**: A user can send a message like "Complete task 1", and the task's status will be updated in the database.

- [X] T013 [US3] Implement the `complete_task` function in `backend/app/tools/task_tools.py`.
- [X] T014 [US3] Add the `complete_task` tool to the agent in `backend/app/api/endpoints/chat.py`.
- [X] T015 [US3] Create a test in `backend/tests/test_chat.py` to verify that the `complete_task` tool works correctly.

## Phase 6: User Story 4 - Delete Task

- **Goal**: Users can delete a task via the chatbot.
- **Independent Test Criteria**: A user can send a message like "Delete task 1", and the task will be removed from the database.

- [X] T016 [US4] Implement the `delete_task` function in `backend/app/tools/task_tools.py`.
- [X] T017 [US4] Add the `delete_task` tool to the agent in `backend/app/api/endpoints/chat.py`.
- [X] T018 [US4] Create a test in `backend/tests/test_chat.py` to verify that the `delete_task` tool works correctly.

## Phase 7: User Story 5 - Update Task

- **Goal**: Users can update a task's title or description via the chatbot.
- **Independent Test Criteria**: A user can send a message like "Update task 1 title to 'Buy groceries'", and the task will be updated in the database.

- [X] T019 [US5] Implement the `update_task` function in `backend/app/tools/task_tools.py`.
- [X] T020 [US5] Add the `update_task` tool to the agent in `backend/app/api/endpoints/chat.py`.
- [X] T021 [US5] Create a test in `backend/tests/test_chat.py` to verify that the `update_task` tool works correctly.

## Phase 8: User Story 6 - Frontend Chat Page

- **Goal**: Users can interact with the chatbot through a web interface.
- **Independent Test Criteria**: The chat page is functional and can send/receive messages to/from the backend.

- [X] T022 [P] [US6] Create the chat page component in `frontend/src/app/[locale]/chat/page.tsx`.
- [X] T023 [US6] Implement the UI for displaying chat messages.
- [X] T024 [US6] Implement the message input form and send button.
- [X] T025 [US6] Implement the API call to the `/api/chat` endpoint.

## Phase 9: Bonus User Story 7 - Urdu Language Support

- **Goal**: The chatbot can respond in Urdu.
- **Independent Test Criteria**: If the user sends a message in Urdu, the chatbot responds in Urdu.

- [X] T026 [P] [US7] Add "ur" to the locales in `frontend/i18n.ts`.
- [X] T027 [US7] Create a `ur.json` file in `frontend/messages` with Urdu translations.
- [X] T028 [US7] Update the agent's system prompt in `backend/app/api/endpoints/chat.py` to instruct it to respond in the user's language.

## Phase 10: Bonus User Story 8 - Voice Commands

- **Goal**: Users can interact with the chatbot using their voice.
- **Independent Test Criteria**: A user can click a button, speak a command, and the transcribed text will be sent to the chatbot.

- [X] T029 [P] [US8] Add a microphone button to the chat input form in `frontend/src/app/[locale]/chat/page.tsx`.
- [X] T030 [US8] Implement the Web Speech API to listen for and transcribe user's voice commands.
- [X] T031 [US8] Send the transcribed text to the chatbot API.

## Phase 11: Polish & Cross-Cutting Concerns

- [X] T032 Review and refine all code for clarity, performance, and adherence to standards.
- [X] T033 Add comprehensive error handling to both the backend and frontend.
- [X] T034 Verify that all user stories are implemented correctly and meet the acceptance criteria.

## Dependencies

- **US2** depends on **US1** (to have tasks to list).
- **US3**, **US4**, **US5** depend on **US1** (to have a task to act upon).
- **US6** depends on all backend user stories (**US1-US5**).
- **US7** and **US8** are independent bonus features.

## Parallel Execution

- Backend tasks (**US1-US5**) can be implemented in parallel with frontend setup (**US6**).
- Within the backend, once the foundational phase is complete, the tool implementation tasks (**T006, T010, T013, T016, T019**) can be done in parallel.

## Implementation Strategy

The implementation will follow an MVP approach, starting with the core backend functionality (adding and listing tasks), then moving to the other CRUD operations, and finally implementing the frontend. The bonus user stories will be addressed last.
