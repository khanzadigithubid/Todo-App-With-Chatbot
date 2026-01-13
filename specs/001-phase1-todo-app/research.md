# Research: Phase I - In-Memory Python Console Todo App

**Feature**: Phase I - In-Memory Python Console Todo App
**Date**: 2025-12-12
**Branch**: 001-phase1-todo-app

## Overview
This document captures all research and technical decisions made during planning for the Phase I in-memory Python console todo application.

## Technical Decisions

### 1. Task Data Model
**Decision**: Use a dataclass for the Task model with fields: id (UUID), title (str), description (Optional[str]), completed (bool), created_at (datetime)

**Rationale**: Dataclasses provide clean, readable code with automatic generation of special methods like __init__ and __repr__. Using UUID for ID ensures uniqueness, and datetime for created_at provides precise timestamping. Optional[str] for description allows it to be nullable as required by the spec.

**Alternatives considered**: 
- Regular class with manual __init__ (more verbose)
- NamedTuple (immutable, which doesn't fit requirements)
- Pydantic model (overkill for this simple use case)

### 2. In-Memory Storage Implementation
**Decision**: Implement InMemoryStorage using Python dictionaries to store tasks with UUID keys

**Rationale**: Simple, fast implementation that meets the "in-memory" requirement without external dependencies. Dictionaries provide O(1) lookup time and are native to Python.

**Alternatives considered**:
- Lists (would require iteration for lookups: O(n))
- Sets (no key-value mapping capability)
- External in-memory store like Redis (requires external dependency, violates in-memory requirement)

### 3. CLI Framework Selection
**Decision**: Use the Typer library for the command-line interface

**Rationale**: Typer is a modern, type-annotated library built on top of Click that provides automatic help generation and type safety. It's recommended by the project constitution (through the Tech Stack Adherence principle) and integrates well with Python's type hints.

**Alternatives considered**:
- Standard argparse (less modern, more verbose)
- Click (used by Typer as foundation, but Typer adds type hints)
- Plain sys.argv (no automatic help generation, no validation)

### 4. Rich UI Components Selection
**Decision**: Use Rich library for tables, panels, and colorful output

**Rationale**: Rich provides beautiful, customizable tables with support for colors, emojis, and formatting as required by the specification. It's explicitly mentioned in the constitution as part of the tech stack.

**Alternatives considered**:
- Standard print statements (no formatting support)
- Colorama + tabulate (requires multiple libraries instead of one)
- Plain text output (doesn't meet requirement for beautiful colored table)

### 5. Dependency Management
**Decision**: Use UV for dependency management as required by constitution

**Rationale**: Project constitution specifically mandates the use of UV for Python dependencies. It's fast and modern, replacing pip in the workflow.

**Alternatives considered**:
- pip (contradicts constitution requirement)
- Poetry (contradicts constitution requirement)

### 6. Validation Implementation
**Decision**: Implement validation in the TodoService layer using custom validation functions

**Rationale**: Keeping validation in the service layer separates business logic from data models and CLI interface. It allows for consistent validation both during creation and updates.

**Alternatives considered**:
- Validation in data models (less flexible for different contexts)
- Validation in CLI layer (not reusable across different interfaces)
- Pydantic validation (overkill for simple string length validation)

### 7. Testing Framework
**Decision**: Use pytest for testing as required by constitution (Code Quality principle)

**Rationale**: Pytest is specified in the constitution under Code Quality & Cleanliness principle. It provides simple syntax, powerful fixtures, and good integration with Python.

**Alternatives considered**:
- Unittest (more verbose, not specified in constitution)
- nose2 (pytest is preferred and constitution-mandated)

### 8. Subagent Architecture
**Decision**: Implement TodoCRUDSubagent as a standalone class in storage.py that handles all persistence operations

**Rationale**: The constitution requires a reusable TodoCRUDSubagent class that will be imported in Phase II-V. Placing it in storage.py makes logical sense as it handles data persistence operations. Making it a separate class allows for easy import and reuse in later phases.

**Alternatives considered**:
- Functions instead of a class (less extensible for later phases)
- Different file location (storage.py is the logical place for persistence operations)

### 9. Multilingual Support Implementation
**Decision**: Create a dedicated module or dictionary structure for Urdu translations of prompts and messages

**Rationale**: Having a centralized translation system makes it easy to maintain and extend multilingual support in the future. It isolates the translation logic from business logic.

**Alternatives considered**:
- Inline translations scattered throughout code (harder to maintain)
- External translation files (unnecessarily complex for initial implementation)