# Implementation Tasks: Phase I - In-Memory Python Console Todo App

**Feature**: Phase I - In-Memory Python Console Todo App
**Status**: TODO
**Date**: 2025-12-12
**Branch**: 001-phase1-todo-app
**Input**: Feature specification from `/specs/phase1/spec.md`, Implementation plan from `/specs/001-phase1-todo-app/plan.md`

## Implementation Strategy

MVP Approach: Implement User Story 1 (Add Task) with all necessary foundational components as a minimum viable product, then incrementally add remaining stories (view, update, delete, complete/incomplete).

**Parallel Execution Opportunities**: Tasks marked with [P] can be executed in parallel as they work with different files and have no dependencies on incomplete tasks.

## Dependencies

- **US1 (Add Task)**: Foundation for all other user stories
- **US2 (View Tasks)**: Depends on US1 (tasks must be able to be created first)
- **US3 (Update Task)**: Depends on US1 (tasks must exist to update)
- **US4 (Delete Task)**: Depends on US1 (tasks must exist to delete)
- **US5 (Complete/Incomplete)**: Depends on US1 (tasks must exist to modify status)

## Phase 1: Setup

Goal: Initialize project structure and configure dependencies

**Independent Test Criteria**: Project structure matches plan, dependencies can be installed with uv, and basic entry point can be run

- [X] T001 Create pyproject.toml with rich, typer, pytest dependencies and start script
- [X] T002 Create project directory structure (src/todo/, tests/)
- [X] T003 Create src/todo/__init__.py file

## Phase 2: Foundational Components

Goal: Implement core data models and storage infrastructure

**Independent Test Criteria**: Task model can be created and validated, InMemoryStorage can store and retrieve tasks

- [X] T004 [P] Implement Task dataclass in src/todo/models.py with id, title, description, completed, created_at
- [X] T005 [P] Implement InMemoryStorage in src/todo/storage.py with dictionary-based storage
- [X] T006 [P] Create reusable TodoCRUDSubagent class in src/todo/storage.py with CRUD operations
- [X] T007 [P] Implement TodoService in src/todo/service.py with validation (title length 1-200 chars)

## Phase 3: User Story 1 - Add Task (Priority: P1)

Goal: Enable users to quickly add a task with title & optional description so they don't forget anything

**Independent Test Criteria**: Can add tasks via CLI with title and optional description, tasks stored with UUID and timestamp, validation prevents invalid titles

- [X] T008 [US1] Implement add command in src/todo/cli.py
- [X] T009 [US1] Handle Urdu prompts for add command ("Title daaliye:")
- [X] T010 [US1] Integrate add command with TodoService and TodoCRUDSubagent
- [X] T011 [US1] Validate title length (1-200 chars) during add operation
- [X] T012 [US1] Test add functionality in tests/test_crud.py

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

Goal: Allow users to see all their tasks in a beautiful colored table so they know what's pending

**Independent Test Criteria**: Can display all tasks in rich, colored table with emojis, completed tasks visually distinguished from pending

- [X] T013 [US2] Implement list command in src/todo/cli.py
- [X] T014 [US2] Create rich table display with emojis (✓ for done, ○ for pending)
- [X] T015 [US2] Add color formatting for different task statuses
- [X] T016 [US2] Include borders and proper table formatting using rich
- [X] T017 [US2] Handle Urdu messages for list command
- [X] T018 [US2] Test list functionality in tests/test_crud.py

## Phase 5: User Story 3 - Update Task (Priority: P2)

Goal: Enable users to update a task by ID when plans change

**Independent Test Criteria**: Can update task details by specifying the task ID, system validates ID existence, appropriate error messages displayed

- [X] T019 [US3] Implement update command in src/todo/cli.py
- [X] T020 [US3] Handle title and description updates with validation
- [X] T021 [US3] Validate that task exists before attempting update
- [X] T022 [US3] Integrate update command with TodoService and TodoCRUDSubagent
- [X] T023 [US3] Handle Urdu prompts and success messages for update
- [X] T024 [US3] Test update functionality in tests/test_crud.py

## Phase 6: User Story 4 - Delete Task (Priority: P2)

Goal: Allow users to delete a task that's no longer needed

**Independent Test Criteria**: Can remove specific task by ID, system validates ID existence, appropriate confirmation/error messages displayed

- [X] T025 [US4] Implement delete command in src/todo/cli.py
- [X] T026 [US4] Validate that task exists before attempting deletion
- [X] T027 [US4] Integrate delete command with TodoCRUDSubagent
- [X] T028 [US4] Handle Urdu prompts and success messages for delete
- [X] T029 [US4] Test delete functionality in tests/test_crud.py

## Phase 7: User Story 5 - Mark Complete/Incomplete (Priority: P3)

Goal: Allow users to mark a task complete/incomplete to feel productive

**Independent Test Criteria**: Can toggle task completion status by specifying the task ID, change reflects in display, system validates ID existence

- [X] T030 [US5] Implement complete command in src/todo/cli.py
- [X] T031 [US5] Implement incomplete command in src/todo/cli.py
- [X] T032 [US5] Validate that task exists before toggling status
- [X] T033 [US5] Integrate toggle commands with TodoCRUDSubagent
- [X] T034 [US5] Handle Urdu prompts and success messages for toggle operations
- [X] T035 [US5] Test complete/incomplete functionality in tests/test_crud.py

## Phase 8: Polish & Cross-Cutting Concerns

Goal: Complete the application with proper error handling, documentation, and multilingual support

**Independent Test Criteria**: All CRUD operations work with appropriate error handling, app runs with uv run main.py, documentation is complete

- [X] T036 [P] Implement graceful error handling for invalid task IDs (red messages)
- [X] T037 [P] Add Urdu translations for all prompts and success messages
- [X] T038 [P] Create main.py with welcome panel and CLI execution
- [X] T039 [P] Create README.md with setup and run instructions
- [X] T040 [P] Create CLAUDE.md documenting TodoCRUDSubagent for Phase II-V reuse
- [X] T041 [P] Add comprehensive tests for all operations in tests/test_crud.py
- [X] T042 [P] Test edge cases (title length validation, non-existent IDs, etc.)
- [X] T043 [P] Verify application runs with "uv run main.py"
- [X] T044 [P] Document any additional functionality in user-stories.md
- [X] T045 [P] Perform final integration testing of all user stories

## Parallel Execution Examples

The following tasks can be worked on in parallel as they operate on different components:

**Group 1 (CLI Commands)**: T008 (add), T013 (list), T019 (update), T025 (delete), T030&T031 (complete/incomplete)
**Group 2 (Testing)**: T012, T018, T024, T029, T035, T041 (various test tasks)
**Group 3 (Documentation)**: T037, T039, T040 (Urdu messages, README, CLAUDE.md)