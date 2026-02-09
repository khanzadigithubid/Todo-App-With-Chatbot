# Troubleshooting Guide for Phase V: Advanced Cloud Deployment

## Common Issues and Solutions

### 1. Kafka Connection Issues

**Problem**: Application fails to connect to Kafka
**Solution**:
- Check if Kafka cluster is running: `kubectl get pods -n kafka`
- Verify Kafka service is accessible: `kubectl get svc -n kafka`
- Ensure the bootstrap server address is correct in your configuration
- Check Kafka logs: `kubectl logs -n kafka deployment/todo-kafka-kafka`

**Problem**: Kafka topics not created automatically
**Solution**:
- Manually create topics using kubectl: `kubectl apply -f k8s/kafka-strimzi.yaml`
- Or create topics via Kafka admin client if using external Kafka

### 2. Dapr Issues

**Problem**: Dapr sidecar not starting
**Solution**:
- Verify Dapr is installed: `dapr status -k`
- Check Dapr system pods: `kubectl get pods -n dapr-system`
- Restart Dapr: `dapr uninstall -k` followed by `dapr init -k`

**Problem**: Dapr components not working
**Solution**:
- Check component status: `kubectl get components.dapr.io`
- Verify component configurations: `kubectl describe component <component-name>`
- Check Dapr logs: `kubectl logs -n dapr-system <dapr-pod-name>`

### 3. Database Connection Issues

**Problem**: Application cannot connect to database
**Solution**:
- Verify database URL is correctly set in environment variables
- Check if database is accessible from the pod: `kubectl exec -it <pod-name> -- nslookup <db-host>`
- Ensure database credentials are correctly configured in secrets

### 4. Deployment Issues

**Problem**: Pods stuck in Pending state
**Solution**:
- Check resource availability: `kubectl describe nodes`
- Verify PersistentVolume availability if using persistent storage
- Check resource quotas: `kubectl describe quota`

**Problem**: Pods crash looping
**Solution**:
- Check pod logs: `kubectl logs <pod-name>`
- Describe pod for events: `kubectl describe pod <pod-name>`
- Verify all required environment variables are set

### 5. Helm Deployment Issues

**Problem**: Helm installation fails
**Solution**:
- Check Helm version compatibility
- Verify all required values are provided: `helm install --dry-run --debug <release-name> <chart-path>`
- Ensure proper RBAC permissions

### 6. Network and Service Issues

**Problem**: Services not accessible
**Solution**:
- Check service status: `kubectl get svc`
- Verify service type and ports: `kubectl describe svc <svc-name>`
- For LoadBalancer services, check if external IP is assigned

**Problem**: Ingress not routing correctly
**Solution**:
- Verify ingress controller is running
- Check ingress rules: `kubectl describe ingress <ingress-name>`
- Verify hostnames and paths in ingress configuration

### 7. Monitoring Issues

**Problem**: Prometheus not scraping metrics
**Solution**:
- Check Prometheus configuration: `kubectl describe configmap prometheus-config`
- Verify service discovery: `kubectl get endpoints <target-service>`
- Check Prometheus logs: `kubectl logs <prometheus-pod>`

## Debugging Commands

### Check Overall System Status
```bash
kubectl get pods --all-namespaces
kubectl get nodes
kubectl get componentstatuses
```

### Check Application Status
```bash
kubectl get pods
kubectl describe deployment todo-backend
kubectl logs deployment/todo-backend
```

### Check Kafka Status
```bash
kubectl get pods -n kafka
kubectl get kafka
kubectl logs -n kafka deployment/todo-kafka-kafka
```

### Check Dapr Status
```bash
dapr status -k
kubectl get pods -n dapr-system
kubectl logs -n dapr-system <dapr-sidecar-pod>
```

### Check Service Connectivity
```bash
kubectl run debug --image=curlimages/curl -it --rm -- curl -v http://todo-backend-service:8000
```

## Performance Tuning

### Kafka Performance
- Adjust partition count based on throughput requirements
- Tune replication factor for durability vs performance
- Monitor broker metrics for resource utilization

### Dapr Performance
- Configure component-specific performance settings
- Use state store partitioning for high-throughput scenarios
- Optimize pub/sub delivery guarantees based on requirements

### Kubernetes Resource Optimization
- Set appropriate resource requests and limits
- Configure HPA for auto-scaling based on metrics
- Use node selectors for workload placement

## Security Considerations

### Secrets Management
- Never commit secrets to version control
- Use Kubernetes secrets or external secret stores
- Rotate secrets regularly

### Network Policies
- Implement network policies to restrict traffic
- Use service mesh for advanced traffic control
- Enable mTLS for service-to-service communication

### Dapr Security
- Configure trust domains for multi-tenant scenarios
- Use scoped components to limit access
- Regularly update Dapr runtime for security patches

## Scaling Recommendations

### Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Kafka Scaling
- Increase broker count for higher throughput
- Adjust partition count for parallel processing
- Configure proper replication for fault tolerance

### Database Scaling
- Use read replicas for read-heavy workloads
- Implement connection pooling
- Consider sharding for very large datasets