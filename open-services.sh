#!/bin/bash

echo "🚀 Abriendo Jaeger..."
minikube service jaeger-service -n opentelemetry &

echo "📊 Abriendo Grafana..."
minikube service grafana-service -n application &

echo "📈 Abriendo Prometheus..."
minikube service prometheus-service -n monitoring &

echo "ejecutando aplicacion de mareas" 
minikube service clima-app-service --url -n application


echo "✅ Todos los servicios se están abriendo en segundo plano."

