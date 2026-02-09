# Demo Script: Todo App with Chatbot - Phase V Features

## Introduction
Welcome to the demonstration of the Todo App with Chatbot - Phase V: Advanced Cloud Deployment. Today we'll showcase the advanced features including recurring tasks, due date reminders, event-driven architecture with Kafka, and Dapr integration.

## Prerequisites for Demo
- Minikube running with the application deployed
- Dapr installed and configured
- Kafka cluster running
- Application accessible via web interface

## Demo Steps

### Step 1: Show the Enhanced UI
1. Navigate to the application in the browser
2. Highlight the new features in the UI:
   - Priority selection
   - Category/tags functionality
   - Due date picker
   - Recurring task toggle

### Step 2: Create a Recurring Task
1. In the chat interface, ask the AI assistant:
   ```
   "Add a recurring task to water my plants every day at 8 AM"
   ```
2. Show how the AI recognizes the recurring nature and due time
3. Demonstrate how the task appears in the task list
4. Explain how the recurring task service will automatically create the next occurrence when this one is completed

### Step 3: Create a Task with Due Date and Reminder
1. Ask the AI assistant:
   ```
   "Create a task to prepare quarterly report due tomorrow at 5 PM"
   ```
2. Show how the task appears with due date
3. Explain how the reminder service will trigger a notification before the due time
4. Demonstrate the event being published to the Kafka "reminders" topic

### Step 4: Complete a Recurring Task
1. Mark the "water plants" task as complete
2. Show how the system automatically generates the next occurrence
3. Explain the event-driven architecture: how completing the task triggered an event in Kafka, which was processed by the recurring task service
4. Demonstrate the new task appearing in the list

### Step 5: Demonstrate Event-Driven Architecture
1. Open a terminal and monitor the Kafka topics:
   ```bash
   kubectl -n kafka run kafka-consumer -ti --image=strimzi/kafka:latest-kafka-3.6.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server todo-kafka-kafka:9092 --topic task-events
   ```
2. Perform a task operation (create/update/delete) in the UI
3. Show how the corresponding event appears in the Kafka consumer
4. Explain how other services can consume these events independently

### Step 6: Show Dapr Integration
1. Demonstrate service-to-service communication via Dapr:
   - How the frontend communicates with the backend through Dapr service invocation
   - How state is managed through Dapr state store
   - How secrets are accessed through Dapr secret store
2. Show Dapr dashboard (if available):
   ```bash
   dapr dashboard
   ```

### Step 7: Scale the Application
1. Show the current replica count:
   ```bash
   kubectl get pods
   ```
2. Scale the application:
   ```bash
   kubectl scale deployment todo-backend --replicas=3
   ```
3. Show the new pods being created
4. Explain how the event-driven architecture handles scaling gracefully

### Step 8: Monitoring and Observability
1. Access the Prometheus dashboard:
   ```bash
   minikube service prometheus-service -n monitoring
   ```
2. Show application metrics
3. Explain how the system is observable and monitorable

## Key Points to Emphasize

### Event-Driven Architecture Benefits
- Loose coupling between services
- Scalability - services can scale independently
- Resilience - if one service is down, events are queued for processing
- Extensibility - new services can consume events without changing existing services

### Dapr Benefits
- Removes infrastructure concerns from application code
- Enables polyglot development
- Provides enterprise capabilities (retry, circuit breaker, etc.) out of the box
- Vendor portability - can switch underlying infrastructure without code changes

### Advanced Features Value
- Recurring tasks automate repetitive work
- Due date reminders help with time management
- Proper architecture supports growth and complexity

## Expected Outcomes
By the end of this demo, viewers should understand:
1. How the advanced features enhance user productivity
2. How event-driven architecture improves system scalability and resilience
3. How Dapr simplifies distributed application development
4. How the system can be deployed and scaled in cloud environments

## Q&A Preparation
Be ready to answer questions about:
- How the recurring task logic handles edge cases
- Performance characteristics under load
- Security considerations
- Future extensibility of the system
- Comparison with traditional monolithic architectures