# scripts/setup-minikube.sh
#!/bin/bash

echo "Setting up Todo App with Chatbot on Minikube..."

# Start Minikube
echo "Starting Minikube..."
minikube start

# Enable required Minikube addons
minikube addons enable ingress
minikube addons enable metrics-server

# Install Strimzi Kafka operator
echo "Installing Strimzi Kafka operator..."
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka

# Deploy Kafka cluster
echo "Deploying Kafka cluster..."
kubectl apply -f k8s/kafka-strimzi.yaml

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka

# Install Dapr
echo "Installing Dapr..."
dapr init -k

# Wait for Dapr to be ready
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=dapr -n dapr-system --timeout=300s

# Deploy Dapr components
echo "Deploying Dapr components..."
kubectl apply -f dapr/components/

# Build and deploy the application
echo "Building and deploying the application..."
kubectl apply -f k8s/backend-deployment.yaml

# Wait for the application to be ready
echo "Waiting for application to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=300s

echo "Setup complete! Your Todo App with Chatbot is now running on Minikube."
echo "To access the application, run: minikube service todo-backend-service"