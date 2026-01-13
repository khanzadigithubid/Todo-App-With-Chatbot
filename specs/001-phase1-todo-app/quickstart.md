# Quickstart: Phase I - In-Memory Python Console Todo App

**Feature**: Phase I - In-Memory Python Console Todo App
**Date**: 2025-12-12
**Branch**: 001-phase1-todo-app

## Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Terminal/command prompt access

## Setup

### 1. Install Dependencies
```bash
uv sync
```

### 2. Install in Development Mode
```bash
uv build
uv pip install -e .
```

## Running the Application

### Method 1: Direct Python Execution
```bash
uv run main.py
```

### Method 2: Using Project Script
```bash
uv run start
```

## Commands

Once the application is running, you can use the following commands:

### Add a Task
```bash
uv run main.py add "Task title here" --description "Optional description here"
```

### List All Tasks
```bash
uv run main.py list
```

### Update a Task
```bash
uv run main.py update <task_id> --title "New title" --description "New description"
```

### Delete a Task
```bash
uv run main.py delete <task_id>
```

### Mark Task as Complete/Incomplete
```bash
# Mark as complete
uv run main.py complete <task_id>

# Mark as incomplete
uv run main.py incomplete <task_id>
```

### Help
```bash
uv run main.py --help
```

## Project Structure
```
.
├── pyproject.toml          # Project configuration and dependencies
├── main.py                 # Entry point application
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py       # Task dataclass definition
│       ├── storage.py      # InMemoryStorage + TodoCRUDSubagent class
│       ├── service.py      # TodoService with validation logic
│       └── cli.py          # Typer CLI application
├── tests/
│   └── test_crud.py        # Pytest tests for all operations
├── README.md               # Setup and run instructions
└── CLAUDE.md               # Documentation for TodoCRUDSubagent reuse
```

## Testing

Run all tests:
```bash
uv run pytest
```

Run specific test file:
```bash
uv run pytest tests/test_crud.py
```

Run tests with coverage:
```bash
uv run pytest --cov=src/todo
```

## Development

### Adding New Features

1. Update the specification in `specs/phase1/spec.md` if needed
2. Update the data model in `specs/phase1/data-model.md` if needed
3. Implement the feature in the appropriate module (models.py, storage.py, service.py, or cli.py)
4. Add tests in `tests/test_crud.py`
5. Update documentation if needed

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public classes and functions
- Use meaningful variable and function names

## Troubleshooting

### Common Issues

1. **Command not found**: Make sure you're using `uv run` to execute commands
2. **Dependency issues**: Run `uv sync` to ensure all dependencies are installed
3. **Invalid task ID**: Ensure you're using the correct UUID format for task operations

### Getting Task IDs

Use the `list` command to see all tasks with their IDs:
```bash
uv run main.py list
```