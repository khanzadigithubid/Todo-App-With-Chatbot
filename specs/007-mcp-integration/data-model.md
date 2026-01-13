# Data Model: MCP Server Integration for Chatbot

## Entities

### Task
Represents a user's task with attributes like title, description, status, priority, and due date

**Fields**:
- id: UUID (Primary Key) - Unique identifier for the task
- user_id: UUID (Foreign Key) - Links task to a user
- title: String (Required) - Title of the task (1-200 characters)
- description: String (Optional) - Detailed description of the task
- status: String (Default: "pending") - Current status ("pending", "completed")
- priority: String (Default: "medium") - Priority level ("low", "medium", "high")
- categories: List[String] (Optional) - Categories/tags associated with the task
- is_recurring: Boolean (Default: false) - Whether the task repeats
- recurrence_pattern: String (Optional) - Pattern if recurring ("daily", "weekly", "monthly")
- created_at: DateTime (Default: now) - Timestamp of creation
- due_date: DateTime (Optional) - Deadline for the task
- updated_at: DateTime (Default: now) - Timestamp of last update

**Validation Rules**:
- Title must be between 1 and 200 characters
- Status must be one of the allowed values
- Priority must be one of the allowed values
- User_id must reference an existing user

**State Transitions**:
- pending → completed (via toggle completion)
- completed → pending (via toggle completion)

### User
Represents a user account with tasks associated to them

**Fields**:
- id: UUID (Primary Key) - Unique identifier for the user
- email: String (Required, Unique) - User's email address
- name: String (Required) - User's name
- password: String (Required) - Hashed password
- created_at: DateTime (Default: now) - Timestamp of account creation

**Validation Rules**:
- Email must be unique and valid format
- Password must be properly hashed
- Name must not be empty

### Standardized Tool
Represents a standardized interface for task operations that connects to the data storage

**Fields**:
- name: String (Required) - Name of the tool (e.g., "add_task", "list_tasks")
- description: String (Required) - Description of what the tool does
- parameters: Object (Required) - Schema defining the parameters the tool accepts
- return_value: Object (Required) - Schema defining the return value of the tool
- implementation_path: String (Required) - Path to the implementation function

**Validation Rules**:
- Name must be unique within the system
- Parameters and return_value must follow MCP protocol specifications
- Implementation_path must reference a valid function

### Chatbot Agent
Represents the AI component that processes natural language and calls standardized tools

**Fields**:
- id: UUID (Primary Key) - Unique identifier for the agent instance
- model: String (Required) - Name of the AI model being used
- configuration: JSON (Required) - Configuration parameters for the agent
- created_at: DateTime (Default: now) - Timestamp of creation

**Validation Rules**:
- Model must be a supported AI model
- Configuration must be valid for the specified model