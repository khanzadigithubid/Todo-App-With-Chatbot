# scripts/deploy-cloud.sh
#!/bin/bash

# Script to deploy the Todo App to cloud Kubernetes (AKS/GKE)
# This script assumes you have already configured kubectl to connect to your cloud cluster

echo "Deploying Todo App with Chatbot to Cloud Kubernetes..."

# Install Dapr on the cloud cluster
echo "Installing Dapr on cloud cluster..."
dapr init -k

# Wait for Dapr to be ready
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=dapr -n dapr-system --timeout=300s

# Deploy Dapr components
echo "Deploying Dapr components..."
kubectl apply -f dapr/components/

# If using self-hosted Kafka, deploy it
# For this example, we'll assume Kafka is externally managed (e.g., Redpanda Cloud)
# If you want to deploy Kafka in-cluster, uncomment the following lines:
# kubectl create namespace kafka
# kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
# kubectl apply -f k8s/kafka-strimzi.yaml
# kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka

# Update deployment with cloud-specific configurations
echo "Updating deployment with cloud configurations..."

# Deploy the application using Helm
echo "Deploying application with Helm..."
helm upgrade --install todo-app ./charts/todo-app -f k8s/cloud-values.yaml --wait

echo "Deployment to cloud complete!"
echo "Application is now running on your cloud Kubernetes cluster."