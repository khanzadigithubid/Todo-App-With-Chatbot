# User Stories: Interactive Terminal Menu for Todo App

## Overview
This document details the user stories for converting the CLI application from a Typer command-based interface to a fully interactive terminal menu system.

## User Stories Table

| ID | User Story | Priority | Acceptance Criteria | Status |
|----|------------|----------|-------------------|--------|
| US-001 | As a user, when I run `uv run main.py`, I want to see an interactive numbered menu so I can easily select what to do next | P1 | Application starts with numbered menu interface instead of command-line options | Pending |
| US-002 | As a user, when I select option 1 from the menu, I want to be prompted for task details so I can add a new task | P1 | Selecting option 1 prompts for title and description, creates task with provided details | Pending |
| US-003 | As a user, when I select option 2 from the menu, I want to see all my tasks displayed in a readable format | P1 | Selecting option 2 displays all tasks with numbers for identification | Pending |
| US-004 | As a user, when I select option 3 from the menu, I want to update an existing task by selecting it and providing new details | P2 | Selecting option 3 prompts for task number and new details, updates specified task | Pending |
| US-005 | As a user, when I select option 4 from the menu, I want to delete an existing task by selecting it | P2 | Selecting option 4 prompts for task number, removes specified task from system | Pending |
| US-006 | As a user, when I select option 5 from the menu, I want to mark a task as complete | P2 | Selecting option 5 prompts for task number, changes status to completed | Pending |
| US-007 | As a user, when I select option 6 from the menu, I want to mark a task as incomplete | P2 | Selecting option 6 prompts for task number, changes status to incomplete | Pending |
| US-008 | As a user, when I select option 7 from the menu, I want to exit the application | P1 | Selecting option 7 terminates the application gracefully | Pending |

## Acceptance Criteria Checklist

- [ ] Running `uv run main.py` displays the interactive menu immediately
- [ ] Menu shows options 1-7 with appropriate labels
- [ ] Option 1 (Add Task) prompts for title and description, creates task
- [ ] Option 2 (List Tasks) displays all tasks in readable format
- [ ] Option 3 (Update Task) prompts for task number and new details
- [ ] Option 4 (Delete Task) prompts for task number and removes task
- [ ] Option 5 (Complete Task) prompts for task number and updates status
- [ ] Option 6 (Mark Incomplete) prompts for task number and updates status
- [ ] Option 7 (Exit) cleanly terminates the application
- [ ] All input is validated and errors are handled gracefully
- [ ] All existing functionality remains intact after conversion
- [ ] Urdu prompts continue to work in the new interface

## Validation Scenarios

### Menu Display
- Given: User runs `uv run main.py`
- When: Application starts
- Then: Numbered menu with options 1-7 is displayed with "Choose an option:" prompt

### Add Task Flow
- Given: User sees the main menu
- When: User selects option 1 and enters valid title and description
- Then: Task is created and success message is displayed, returning to main menu

### List Tasks Flow
- Given: User has tasks in the system
- When: User selects option 2
- Then: All tasks are displayed with numbering, returning to main menu after viewing

### Update Task Flow
- Given: User has tasks in the system
- When: User selects option 3 and enters valid task number with new details
- Then: Task is updated and confirmation is displayed, returning to main menu

### Exit Flow
- Given: User is at the main menu
- When: User selects option 7
- Then: Application exits cleanly

## Edge Cases to Handle

- Invalid menu selection (non-numeric input)
- Non-existent task numbers when updating/deleting
- Empty or extremely long task titles/descriptions
- Terminal window resizing during interaction
- User entering blank responses when prompted for required fields