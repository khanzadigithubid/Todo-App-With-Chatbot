# Quickstart Guide: MCP Server Integration for Chatbot

## Overview
This guide provides instructions to quickly set up and run the MCP-integrated chatbot system. The implementation replaces direct tool calls with standardized MCP tools for task management operations.

## Prerequisites
- Python 3.13+
- Node.js 18+ and npm
- Docker and Docker Compose
- Neon Postgres DB account
- OpenAI API key
- MCP SDK

## Setup Instructions

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd hackathon2-p3

# Set up Python environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 2. Configuration
Create a `.env` file in the backend directory with the following variables:
```env
NEON_DATABASE_URL=your_neon_db_connection_string
OPENAI_API_KEY=your_openai_api_key
BETTER_AUTH_SECRET=your_auth_secret
MCP_SERVER_URL=your_mcp_server_url
```

### 3. Database Setup
```bash
# Run the backend to initialize the database
cd backend
uv run python -m app.main
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Running the Application
```bash
# Terminal 1: Start the backend
cd backend
uv run python -m app.main

# Terminal 2: Start the frontend
cd frontend
npm run dev
```

## Key Components

### MCP Tools
The system includes the following MCP tools for task management:
- `add_task`: Create new tasks
- `list_tasks`: Retrieve user's tasks
- `update_task`: Modify existing tasks
- `delete_task`: Remove tasks
- `toggle_task_completion`: Change task completion status

### Architecture
- **Backend**: FastAPI application with MCP tools in `/tools` directory
- **Frontend**: Next.js application with unchanged UI
- **Database**: Neon Postgres DB with existing schema
- **Agent**: Updated to use MCP SDK for tool calls

## Testing the Integration
1. Access the chatbot interface at `http://localhost:3000`
2. Authenticate with your credentials
3. Try natural language commands like:
   - "Add a task: Buy groceries"
   - "Show my tasks"
   - "Complete task 1"
   - "Update task 1 to have high priority"

## Troubleshooting
- If MCP tools aren't responding, verify that the MCP server is running
- Check that the `.env` variables are correctly set
- Ensure the database connection is working
- Review the logs in both frontend and backend for error messages