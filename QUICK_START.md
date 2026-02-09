# Phase V Quick Start Guide

## Getting Started with Advanced Cloud Deployment

This guide will help you quickly set up the Todo App with Chatbot featuring advanced capabilities like recurring tasks, due date reminders, event-driven architecture with Kafka, and Dapr integration.

## Prerequisites

Before starting, ensure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Kubernetes enabled
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for local deployment)

## Option 1: Local Setup with Minikube (Recommended for Development)

### Step 1: Start Minikube
```bash
minikube start
```

### Step 2: Make the setup script executable and run it
```bash
chmod +x scripts/setup-minikube.sh
./scripts/setup-minikube.sh
```

This script will:
- Install Strimzi Kafka operator
- Deploy Kafka cluster
- Install Dapr
- Deploy Dapr components
- Deploy the Todo application

### Step 3: Access the Application
```bash
minikube service todo-backend-service
```

## Option 2: Manual Setup (Step-by-step)

### Step 1: Install Strimzi Kafka Operator
```bash
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
```

### Step 2: Deploy Kafka Cluster
```bash
kubectl apply -f k8s/kafka-strimzi.yaml
```

Wait for Kafka to be ready:
```bash
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka
```

### Step 3: Install Dapr
```bash
dapr init -k
```

Wait for Dapr to be ready:
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=dapr -n dapr-system --timeout=300s
```

### Step 4: Deploy Dapr Components
```bash
kubectl apply -f dapr/components/
```

### Step 5: Build and Deploy the Application
```bash
# Build the Docker image
cd backend
docker build -t todo-backend:latest .
cd ..

# Deploy using Helm
helm install todo-app ./charts/todo-app -f k8s/local-values.yaml
```

## Configuration

### Environment Variables
Update the `k8s/local-values.yaml` file with your specific configurations:

```yaml
# Database configuration - update with your local database URL
database:
  url: "postgresql://username:password@neon-db-host:5432/todo_local"  # Update with your local DB URL

# Authentication configuration
auth:
  secret: "your-local-auth-secret"  # Update with your local auth secret

# OpenAI configuration
openai:
  apiKey: "your-openai-api-key"  # Update with your OpenAI API key
```

### Kafka Configuration
The default configuration uses Kafka deployed in the same cluster. If you want to use an external Kafka (like Redpanda Cloud), update the bootstrap server in `k8s/local-values.yaml`:

```yaml
kafka:
  bootstrapServers: "your-redpanda-cluster.example.com:9092"  # Update with your Kafka/Redpanda endpoint
```

## Verifying the Setup

### Check All Pods Are Running
```bash
kubectl get pods
```

You should see pods for:
- todo-backend
- kafka (Strimzi)
- Dapr system pods in the dapr-system namespace

### Check Dapr Components
```bash
kubectl get components.dapr.io
```

### Test the Application
1. Get the service URL: `minikube service todo-backend-service --url`
2. Visit the URL in your browser
3. Try creating a task with the AI assistant:
   - "Create a task to water my plants every day at 8 AM"
   - "Set a reminder to call mom tomorrow at 7 PM"

## Key Features to Explore

### 1. Recurring Tasks
Ask the AI: "Create a recurring task to backup files every Sunday at 2 AM"
- Notice how the task is marked as recurring
- When you complete it, a new occurrence will be automatically created

### 2. Due Date Reminders
Ask the AI: "Create a task to submit report due tomorrow at 5 PM"
- The system will schedule a reminder for the specified time

### 3. Event-Driven Architecture
- All task operations generate events published to Kafka
- These events can be consumed by other services independently
- Check the Kafka topics to see the events: `kubectl -n kafka run kafka-consumer -ti --image=strimzi/kafka:latest-kafka-3.6.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server todo-kafka-kafka:9092 --topic task-events`

### 4. Dapr Integration
- Services communicate through Dapr without direct dependencies
- State is managed through Dapr state store
- Secrets are accessed through Dapr secret store

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**: Check available resources with `kubectl describe nodes`

2. **Kafka not ready**: Verify Strimzi operator is installed and Kafka CRDs are available

3. **Dapr sidecar not injected**: Ensure Dapr is installed with `dapr status -k`

4. **Application can't connect to Kafka**: Check Kafka service name and port in application configuration

### Useful Commands
```bash
# Check logs of the main application
kubectl logs deployment/todo-backend

# Check Dapr logs
kubectl logs -n dapr-system <dapr-sidecar-pod>

# Check Kafka logs
kubectl logs -n kafka deployment/todo-kafka-kafka

# Port forward to access the application directly
kubectl port-forward service/todo-backend-service 8000:8000
```

## Next Steps

Once you have the local setup working, you can:

1. Explore the advanced features in the UI
2. Look at the event-driven architecture by monitoring Kafka topics
3. Experiment with scaling the application
4. Review the monitoring setup with Prometheus
5. Prepare for cloud deployment by reviewing `k8s/cloud-values.yaml`

## Moving to Cloud Deployment

When ready to deploy to cloud (AKS/GKE):

1. Update `k8s/cloud-values.yaml` with your cloud-specific configurations
2. Ensure your cloud cluster has Dapr installed: `dapr init -k`
3. Use the cloud deployment script: `./scripts/deploy-cloud.sh` (after making it executable)

For more details on cloud deployment, refer to the main README.md file.