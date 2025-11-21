
# Proyecto de Clima y Mareas 🌤️🌊

## Descripción
Este proyecto es una aplicación web desarrollada en **Python + Streamlit**, instrumentada con **OpenTelemetry**, y desplegada con **Kubernetes (Minikube)**.  
Incluye observabilidad completa con **Prometheus**, **Grafana** y **Jaeger**.

La aplicación muestra:
- Datos del clima (temperatura, humedad, presión) usando OpenWeather API.
- Gráfico con próximas mareas usando WorldTides API.
- Métricas expuestas mediante OpenTelemetry.
- Dashboards y alertas en Grafana.
- Trazas distribuidas en Jaeger.

---

## Tecnologías Utilizadas
- **Python 3**
- **Streamlit**
- **Flask**
- **OpenTelemetry SDK + Collector**
- **Prometheus**
- **Grafana**
- **Jaeger**
- **Kubernetes (Minikube)**
- **Docker**

---

## Estructura del Proyecto
```
Proyecto-de-clima/
├── Main.py                    # Aplicación principal
├── Dockerfile                 # Imagen Docker
├── deployment.yaml            # Deployment de Kubernetes
├── service.yaml               # Servicio de la app
├── prometheus.yaml            # Scrape configs
├── otel-collector.yaml        # OTEL Collector (traces + metrics)
├── grafana-dashboard.yaml     # Dashboards y alertas
├── requirements.txt           # Dependencias Python
└── README.md
```

---

## Instalación y Ejecución Local (Docker)

### 1. Clonar repositorio
```bash
git clone https://github.com/JoswardSilva/Proyecto-de-clima
cd Proyecto-de-clima
```

### 2. Construir imagen Docker
```bash
docker build -t clima-app .
```

### 3. Ejecutar aplicación
```bash
docker run --rm -p 8501:8501 clima-app
```

Abrir en navegador:
```
http://localhost:8501
```

---

## Despliegue Completo en Kubernetes (Minikube)

### 1. Iniciar Minikube
```bash
minikube start
```

### 2. Aplicar manifiestos
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f prometheus.yaml
kubectl apply -f grafana-dashboard.yaml
kubectl apply -f otel-collector.yaml
```

### 3. Verificar
```bash
kubectl get pods -A
```

### 4. Abrir servicios
Prometheus:
```bash
minikube service prometheus-service -n monitoring
```

Grafana:
```bash
minikube service grafana-service -n application
```

Jaeger:
```bash
minikube service jaeger-service -n application
```

Aplicación:
```bash
minikube service clima-app-service -n application
```

---

## Observabilidad

### Trazas – Jaeger
La app envía trazas instrumentadas automáticamente usando OTLP → OTEL Collector → Jaeger.

### Métricas – Prometheus
Prometheus captura:
- Métricas internas del OTEL Collector  
- Métricas generadas desde spanmetrics  
- Métricas expuestas por la app  

### Dashboards – Grafana
Incluye dashboards listos para:
- CPU usage  
- Pod CPU usage  
- Estado de la app `clima-app`  
- Dashboards SRE (SLI/SLO/Error Budget)  
- Alertas integradas  

---

## Dependencias Python
```bash
pip install -r requirements.txt
```

---

## Licencia
MIT License.

---

## Autor
**José Silva**
