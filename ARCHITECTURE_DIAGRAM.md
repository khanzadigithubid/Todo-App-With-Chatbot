# Phase V: Advanced Cloud Deployment - Architecture Diagram

## High-Level Architecture

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
│                    │  │ task-events │  │     reminders       │  │ task-updates    │ │
│                    │  └─────────────┘  └─────────────────────┘  └─────────────────┘ │
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

## Component Details

### Frontend Service
- Next.js application with AI chat interface
- Communicates with backend via Dapr service invocation
- Real-time updates via WebSocket connections

### Backend Service  
- FastAPI application with MCP and AI integration
- Task CRUD operations with event publishing
- Dapr sidecar for infrastructure abstractions

### Dapr Runtime Layer
- Provides building blocks as sidecars
- Abstracts infrastructure concerns (Kafka, DB, Secrets)
- Enables language-agnostic microservices

### Event Processing Services
- Recurring Task Service: Processes completed recurring tasks and creates next occurrences
- Reminder Service: Handles due date notifications
- Audit Service: Maintains complete history of operations
- WebSocket Service: Broadcasts updates to connected clients

### Kafka/Redpanda Cluster
- Event streaming platform for asynchronous communication
- Topics for different event types (task-events, reminders, task-updates)
- Enables loose coupling and scalability

### External Services
- Neon PostgreSQL: Primary data storage
- OpenAI API: AI assistant capabilities
- Cloud Storage: File attachments and media

## Event Flows

### 1. Task Creation Flow
User Input → Frontend → Dapr Service Invoke → Backend → Kafka Producer → task-events Topic → Event Processing Services

### 2. Recurring Task Flow
Task Completed → Kafka Event → Recurring Task Service → New Task Created → Kafka Event → task-events Topic

### 3. Reminder Flow
Task with Due Date → Kafka Event → reminders Topic → Reminder Service → Notification to User

### 4. Real-time Sync Flow
Task Updated → Kafka Event → task-updates Topic → WebSocket Service → All Connected Clients

## Deployment Environments

### Local (Minikube)
- Single-node Kubernetes cluster
- Strimzi for Kafka deployment
- Local Dapr installation
- Neon DB as external service

### Cloud (AKS/GKE)
- Multi-node production cluster
- Redpanda Cloud for Kafka
- Managed Dapr installation
- Production-grade configurations
- Monitoring and logging

## Key Benefits

1. **Scalability**: Independent scaling of services based on demand
2. **Resilience**: Event-driven architecture with built-in retry mechanisms
3. **Maintainability**: Clear separation of concerns with microservices
4. **Flexibility**: Dapr enables technology swaps without code changes
5. **Observability**: Comprehensive monitoring and logging capabilities
6. **Security**: Dapr provides mTLS and secure secret management