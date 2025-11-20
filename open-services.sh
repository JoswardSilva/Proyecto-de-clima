#!/bin/bash

echo "🚀 Abriendo Jaeger..."
minikube service jaeger-service -n opentelemetry &

echo "📊 Abriendo Grafana..."
minikube service grafana-service -n monitoring &

echo "📈 Abriendo Prometheus..."
minikube service prometheus-service -n monitoring &


echo "✅ Todos los servicios se están abriendo en segundo plano."

