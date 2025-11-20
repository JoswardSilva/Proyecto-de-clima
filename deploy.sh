#!/bin/bash
set -euo pipefail

IMAGE_NAME=joscloks418/clima-app:latest

echo "Building Docker image..."
docker build -t $IMAGE_NAME .
echo "Pushing image to Docker Hub..."
docker push $IMAGE_NAME

echo "Applying Kubernetes manifests..."
kubectl apply -f otel-collector.yaml
kubectl apply -f jaeger.yaml
kubectl apply -f deployment.yaml
kubectl apply -f grafana.yaml

echo "Restarting deployment to pick up latest image..."
kubectl rollout restart deployment/clima-app -n application || true

echo "Done."