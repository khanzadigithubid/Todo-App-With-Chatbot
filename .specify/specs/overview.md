# Hackathon II: Todo App - Specification

## Project Overview
This project implements a Todo application that evolves from a simple console app to a cloud-native AI chatbot deployed on Kubernetes. The application follows a spec-driven development approach using Claude Code and Spec-Kit Plus.

## Project Goals
1. Demonstrate progressive complexity from console app to cloud-native AI system
2. Implement spec-driven development methodology
3. Showcase AI integration at multiple levels
4. Deploy using modern cloud-native technologies

## Feature Progression

### Basic Level Features (Phases I & II)
- Add Task – Create new todo items
- Delete Task – Remove tasks from the list
- Update Task – Modify existing task details
- View Task List – Display all tasks
- Mark as Complete – Toggle task completion status

### Intermediate Level Features (Phase II & III)
- Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
- Search & Filter – Search by keyword; filter by status, priority, or date
- Sort Tasks – Reorder by due date, priority, or alphabetically

### Advanced Level Features (Phase IV & V)
- Recurring Tasks – Auto-reschedule repeating tasks (e.g., "weekly meeting")
- Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications

## Phase Specifications

### Phase I: Todo In-Memory Python Console App
**Objective**: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.

**Requirements**:
- Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
- Use spec-driven development with Claude Code and Spec-Kit Plus
- Follow clean code principles and proper Python project structure

**Technology Stack**:
- UV
- Python 3.13+
- Claude Code
- Spec-Kit Plus

**Deliverables**:
- GitHub repository with:
  - Constitution file
  - specs history folder containing all specification files
  - /src folder with Python source code
  - README.md with setup instructions
  - CLAUDE.md with Claude Code instructions
- Working console application demonstrating:
  - Adding tasks with title and description
  - Listing all tasks with status indicators
  - Updating task details
  - Deleting tasks by ID
  - Marking tasks as complete/incomplete

### Phase II: Todo Full-Stack Web Application
**Objective**: Transform the console app into a modern multi-user web application with persistent storage.

**Requirements**:
- Implement all 5 Basic Level features as a web application
- Create RESTful API endpoints
- Build responsive frontend interface
- Store data in Neon Serverless PostgreSQL database
- Authentication – Implement user signup/signin using Better Auth

**Technology Stack**:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Spec-Driven: Claude Code + Spec-Kit Plus
- Authentication: Better Auth

**API Endpoints**:
- GET /api/{user_id}/tasks - List all tasks
- POST /api/{user_id}/tasks - Create a new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update a task
- DELETE /api/{user_id}/tasks/{id} - Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

### Phase III: Todo AI Chatbot
**Objective**: Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture.

**Requirements**:
- Implement conversational interface for all Basic Level features
- Use OpenAI Agents SDK for AI logic
- Build MCP server with Official MCP SDK that exposes task operations as tools
- Stateless chat endpoint that persists conversation state to database
- AI agents use MCP tools to manage tasks

**Technology Stack**:
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth

**MCP Tools Specification**:
- add_task: Create a new task
- list_tasks: Retrieve tasks from the list
- complete_task: Mark a task as complete
- delete_task: Remove a task from the list
- update_task: Modify task title or description

### Phase IV: Local Kubernetes Deployment
**Objective**: Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube, Helm Charts.

**Requirements**:
- Containerize frontend and backend applications
- Use Docker AI Agent (Gordon) for AI-assisted Docker operations
- Create Helm charts for deployment
- Use kubectl-ai and kagent for AI-assisted Kubernetes operations
- Deploy on Minikube locally

**Technology Stack**:
- Containerization: Docker (Docker Desktop)
- Docker AI: Docker AI Agent (Gordon)
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AI DevOps: kubectl-ai, and Kagent
- Application: Phase III Todo Chatbot

### Phase V: Advanced Cloud Deployment
**Objective**: Implement advanced features and deploy to production-grade Kubernetes.

**Part A: Advanced Features**:
- Implement all Advanced Level features (Recurring Tasks, Due Dates & Reminders)
- Implement Intermediate Level features (Priorities, Tags, Search, Filter, Sort)
- Add event-driven architecture with Kafka
- Implement Dapr for distributed application runtime

**Part B: Local Deployment**:
- Deploy to Minikube
- Deploy Dapr on Minikube with full capabilities

**Part C: Cloud Deployment**:
- Deploy to cloud Kubernetes (Azure AKS/Google GKE)
- Deploy Dapr with full capabilities
- Use Kafka service (Confluent/Redpanda Cloud)
- Set up CI/CD pipeline using Github Actions
- Configure monitoring and logging

## Architecture Overview
The application follows a microservices architecture with:
- Frontend service (Next.js)
- Backend API service (FastAPI)
- Database service (Neon PostgreSQL)
- AI/MCP service (OpenAI Agents + MCP)
- Event streaming (Kafka/Redpanda)
- Service mesh (Dapr)

## Success Criteria
- All phases completed according to specifications
- Proper spec-driven development followed
- Clean, maintainable codebase
- Successful deployment on cloud platforms
- Working AI chatbot functionality
- Proper security implementation
- Scalable architecture