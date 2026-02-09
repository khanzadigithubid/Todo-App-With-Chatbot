# Todo App With Chatbot - Evolution from CLI to Cloud-Native AI

## Project Overview

This project demonstrates the evolution of a simple todo application from a console app to a cloud-native AI chatbot deployed on Kubernetes. It showcases spec-driven development using Claude Code and Spec-Kit Plus, following modern software engineering practices.

## Project Phases

### Phase I: Todo In-Memory Python Console App
- Built a command-line todo application with in-memory storage
- Implemented all 5 basic features: Add, Delete, Update, View, Mark Complete
- Established spec-driven development workflow

### Phase II: Todo Full-Stack Web Application
- Transformed the console app into a modern web application
- Implemented RESTful API with FastAPI and SQLModel
- Added user authentication with Better Auth and JWT tokens
- Created responsive UI with Next.js and Tailwind CSS

### Phase III: Todo AI Chatbot
- Integrated OpenAI ChatKit for conversational interface
- Implemented OpenAI Agents SDK for AI logic
- Built MCP (Model Context Protocol) server with task operation tools
- Created stateless chat endpoint with conversation persistence

### Phase IV: Local Kubernetes Deployment
- Containerized frontend and backend applications
- Created Helm charts for deployment
- Deployed to local Kubernetes cluster using Minikube
- Used AI-assisted Docker operations (Gordon) and Kubernetes operations (kubectl-ai, kagent)

### Phase V: Advanced Cloud Deployment
- Implemented advanced features: recurring tasks, due date reminders
- Added event-driven architecture with Kafka
- Integrated Dapr for distributed application runtime
- Deployed to cloud Kubernetes (AKS/GKE) with monitoring and CI/CD

## Tech Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- OpenAI ChatKit
- Framer Motion (animations)
- Heroicons (UI icons)

### Backend
- Python FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL
- OpenAI Agents SDK
- MCP Protocol
- aiokafka (Kafka integration)
- Dapr (Distributed Application Runtime)

### Infrastructure
- Docker
- Kubernetes (Minikube for local, AKS/GKE for cloud)
- Helm Charts
- Kafka/Redpanda
- Dapr
- kubectl-ai, kagent

### Authentication
- Better Auth with JWT tokens

### Monitoring
- Prometheus (metrics)
- Grafana (dashboards)

## Features

### Basic Level
- Add Task – Create new todo items
- Delete Task – Remove tasks from the list
- Update Task – Modify existing task details
- View Task List – Display all tasks
- Mark as Complete – Toggle task completion status

### Intermediate Level
- Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
- Search & Filter – Search by keyword; filter by status, priority, or date
- Sort Tasks – Reorder by due date, priority, or alphabetically

### Advanced Level
- Recurring Tasks – Auto-reschedule repeating tasks (e.g., "weekly meeting")
- Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications
- Event-Driven Architecture – Kafka-based messaging for task operations
- Dapr Integration – Distributed Application Runtime for microservices

## Architecture

The application follows a microservices architecture with:

- Frontend service (Next.js)
- Backend API service (FastAPI)
- Database service (Neon PostgreSQL)
- AI/MCP service (OpenAI Agents + MCP)
- Event streaming (Kafka/Redpanda)
- Service mesh (Dapr)

### Phase V Architecture Details

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              CLOUD/KUBERNETES CLUSTER                               │
│                                                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────────────┐ │
│  │    Frontend Pod     │  │    Backend Pod      │  │   Notification Service      │ │
│  │ ┌─────────┐ ┌─────┐ │  │ ┌─────────┐ ┌─────┐ │  │        Pod                  │ │
│  │ │ Next.js │ │Dapr │ │  │ │FastAPI  │ │Dapr │ │  │ ┌─────────────┐ ┌─────────┐ │ │
│  │ │  App    │ │Side │ │  │ │+MCP+AI  │ │Side │ │  │ │Notification │ │  Dapr   │ │ │
│  │ │         │ │car  │ │  │ │         │ │car  │ │  │ │   Service   │ │  Side   │ │ │
│  │ └─────────┘ └─────┘ │  │ └─────────┘ └─────┘ │  │ │             │ │  Car    │ │ │
│  └─────────┬───────────┘  └─────────┬───────────┘  │ └─────────────┘ └─────────┘ │ │
│            │                         │              └─────────────┬─────────────────┘ │
│            │                         │                            │                   │
│            └─────────────────────────┼────────────────────────────┼───────────────────┘
│                                      │                            │
│                                      ▼                            ▼
│                    ┌─────────────────────────────┐  ┌─────────────────────────────┐
│                    │      DAPR RUNTIME          │  │      EVENT PROCESSORS       │
│                    │     MICROSERVICES          │  │        SERVICES             │
│                    │                            │  │                             │
│                    │ • Pub/Sub (Kafka)         │  │ • Recurring Task Service    │
│                    │ • State Management        │  │ • Reminder Service          │
│                    │ • Service Invocation      │  │ • Audit Service             │
│                    │ • Secret Management       │  │ • WebSocket Service         │
│                    │ • Job Scheduler           │  │                             │
│                    └─────────────┬─────────────┘  └─────────────┬─────────────────┘
│                                  │                              │
│                                  ▼                              ▼
│                    ┌─────────────────────────────────────────────────────────────────┐
│                    │                KAFKA/REDDRANDA CLUSTER                        │
│                    │  ┌─────────────┐  ┌─────────────────────┐  ┌─────────────────┐ │
│                    │ │ task-events │  │     reminders       │  │ task-updates    │ │
│                    │ └─────────────┘  └─────────────────────┘  └─────────────────┘ │
│                    └─────────────────────────┬───────────────────────────────────────┘
│                                              │
│                                              ▼
│                    ┌─────────────────────────────────────────────────────────────────┐
│                    │                    EXTERNAL SERVICES                          │
│                    │                                                               │
│                    │ • Neon PostgreSQL (Task/Conversation Data)                    │
│                    │ • OpenAI API (AI Assistant)                                   │
│                    │ • Cloud Storage (File Attachments)                            │
│                    └─────────────────────────────────────────────────────────────────┘
└──────────────────────────────────────────────────────────────────────────────────────┘

## Setup Instructions

### Prerequisites
- Node.js 18+ for frontend
- Python 3.13+ for backend
- Docker Desktop with Kubernetes enabled
- kubectl
- Helm
- Neon PostgreSQL account
- Dapr CLI (for Phase V)
- Kafka/Redpanda (for Phase V)

### Phase II Setup (Full-Stack Web App)

1. Clone the repository:
```bash
git clone https://github.com/khanzadigithubid/Todo-App-With-Chatbot.git
cd Todo-App-With-Chatbot
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory:
```env
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=your_jwt_secret
OPENAI_API_KEY=your_openai_api_key
```

4. Start the backend:
```bash
cd backend
python start_server.py
```

5. Set up the frontend:
```bash
cd frontend
npm install
```

6. Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

7. Start the frontend:
```bash
cd frontend
npm run dev
```

The application will be available at http://localhost:3000

### Phase III Setup (AI Chatbot)

1. Ensure your OpenAI API key is set in the backend `.env` file
2. The chatbot functionality is integrated into the web application
3. Access the chatbot through the UI at http://localhost:3000/chat

### Phase IV Setup (Kubernetes)

1. Ensure Minikube is running:
```bash
minikube start
```

2. Install Dapr:
```bash
dapr init -k
```

3. Deploy using Helm:
```bash
helm install todo-app ./charts/todo-app -f ./k8s/local-values.yaml
```

### Phase V Setup (Advanced Cloud Deployment)

#### Local Minikube Setup with Kafka and Dapr

1. Start Minikube:
```bash
minikube start
```

2. Install Strimzi Kafka operator:
```bash
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
```

3. Deploy Kafka cluster:
```bash
kubectl apply -f k8s/kafka-strimzi.yaml
```

4. Install Dapr:
```bash
dapr init -k
```

5. Deploy Dapr components:
```bash
kubectl apply -f dapr/components/
```

6. Deploy the application:
```bash
kubectl apply -f k8s/backend-deployment.yaml
```

#### Cloud Deployment (AKS/GKE)

1. Set up your cloud Kubernetes cluster (AKS/GKE)
2. Install Dapr on the cluster:
```bash
dapr init -k
```

3. Configure Kafka (using Redpanda Cloud or self-hosted)
4. Update the Helm values file with cloud-specific configurations
5. Deploy using Helm:
```bash
helm install todo-app ./charts/todo-app -f ./k8s/cloud-values.yaml
```

#### CI/CD Pipeline

The project includes a GitHub Actions workflow for continuous deployment:
- Automatically builds Docker images on code changes
- Deploys to Kubernetes cluster
- Includes health checks and rollbacks

To use the CI/CD pipeline:
1. Configure your cloud cluster credentials as GitHub secrets
2. Update the deploy.yml workflow with your cluster details
3. Push changes to trigger the pipeline

#### Monitoring and Logging

The application includes monitoring configurations:
- Prometheus for metrics collection
- Preconfigured service discovery for the todo backend
- Ready-to-use Grafana dashboards (can be added separately)

To set up monitoring:
```bash
kubectl apply -f k8s/monitoring.yaml
```

#### Setup Scripts

The project includes scripts to simplify deployment:
- `scripts/setup-minikube.sh` - Sets up the entire application on Minikube with Kafka and Dapr
- `scripts/deploy-cloud.sh` - Deploys the application to cloud Kubernetes (AKS/GKE)

Make the scripts executable before running:
```bash
chmod +x scripts/setup-minikube.sh
chmod +x scripts/deploy-cloud.sh
```

## Spec-Driven Development

This project follows a spec-driven development approach:

1. **Constitution**: Defines project principles and constraints
2. **Specification**: Details requirements and acceptance criteria
3. **Plan**: Outlines architecture and implementation approach
4. **Tasks**: Breaks down work into atomic units
5. **Implementation**: Code implementation following the tasks

All specifications are located in the `.specify/` directory.

## Contributing

This project was developed following spec-driven development principles using Claude Code and Spec-Kit Plus. Contributions should follow the same methodology:

1. Update specifications if adding new features
2. Create or update tasks in the `.specify/tasks/` directory
3. Implement code following the defined tasks
4. Update tests and documentation

## License

This project is part of the Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI by Panaversity.