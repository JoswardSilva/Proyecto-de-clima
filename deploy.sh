#!/bin/bash
set -euo pipefail

# =============================
#   Colores para logs bonitos
# =============================
GREEN="\e[32m"
CYAN="\e[36m"
YELLOW="\e[33m"
RED="\e[31m"
RESET="\e[0m"

log() {
    echo -e "${CYAN}🔧 $1${RESET}"
}

success() {
    echo -e "${GREEN}✅ $1${RESET}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${RESET}"
}

error() {
    echo -e "${RED}❌ $1${RESET}"
}

# =============================
#   VARIABLES
# =============================
IMAGE_NAME="joscloks418/clima-app:latest"
NAMESPACE_APP="application"
NAMESPACE_OTEL="opentelemetry"
NAMESPACE_MONITORING="monitoring"

# =============================
#   VALIDACIONES
# =============================

if ! command -v minikube >/dev/null 2>&1; then
    error "Minikube no está instalado."
    exit 1
fi

if ! minikube status >/dev/null 2>&1; then
    error "Minikube no está corriendo. Ejecuta: minikube start"
    exit 1
fi

log "Usando Docker dentro de Minikube..."
eval "$(minikube docker-env)"

# =============================
#   BUILD + PUSH
# =============================

log "Construyendo imagen Docker..."
docker build -t "$IMAGE_NAME" .

log "Pushing a DockerHub..."
docker push "$IMAGE_NAME"

success "Imagen lista: $IMAGE_NAME"

# =============================
#   CREAR NAMESPACES
# =============================

log "Creando namespaces (si no existen)..."
kubectl create namespace $NAMESPACE_APP --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace $NAMESPACE_OTEL --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace $NAMESPACE_MONITORING --dry-run=client -o yaml | kubectl apply -f -

# =============================
#   APLICAR MANIFESTS EN ORDEN
# =============================

log "Aplicando configuración de OTEL Collector..."
kubectl apply -f otel-collector.yaml

log "Aplicando Jaeger..."
kubectl apply -f jaegar.yaml

log "Aplicando clima-app..."
kubectl apply -f deployment.yaml

log "Aplicando Grafana..."
kubectl apply -f grafana.yaml

log "Aplicando Prometheus..."
kubectl apply -f prometheus.yaml

log "Aplicando clima-app..."
kubectl apply -f configmap-clima.yaml

# =============================
#   RESTART DEPLOYMENT
# =============================

log "Reiniciando clima-app para cargar la nueva imagen..."
kubectl rollout restart deployment/clima-app -n $NAMESPACE_APP || true

# =============================
#   ESPERAR PODS
# =============================

log "Esperando a que los pods estén listos..."
kubectl wait --for=condition=available --timeout=120s deployment/clima-app -n $NAMESPACE_APP || warn "clima-app tomó demasiado tiempo."
kubectl wait --for=condition=available --timeout=120s deployment/prometheus-deployment -n $NAMESPACE_MONITORING || true
kubectl wait --for=condition=available --timeout=120s deployment/grafana -n $NAMESPACE_APP || true
kubectl wait --for=condition=available --timeout=120s deployment/otel-collector -n $NAMESPACE_OTEL || true


success "Despliegue completo."
success "Todo está funcionando correctamente 🎉, ejecuta ./open-services.sh para ver todas las URLs y poder acceder"
