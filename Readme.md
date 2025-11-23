# Proyecto de Clima y Mareas 🌤️🌊

## Descripción
Este proyecto es una aplicación web desarrollada en **Python + Streamlit**, instrumentada con **OpenTelemetry**, y desplegada con **Kubernetes (Minikube)**. Incluye observabilidad completa con **Prometheus**, **Grafana** y **Jaeger**.

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
├── configmap-clima.yaml       # ConfigMap sin datos sensibles
├── requirements.txt           # Dependencias Python
├── grafana.yaml               # Dashboards y alertas
├── prometheus.yaml            # Scrape configs
├── otel-collector.yaml        # OTEL Collector (traces + metrics)
├── .env.example               # Ejemplo de variables de entorno
└── README.md
```

---

## Instalación y Ejecución Local (Docker)

### 1. Clonar repositorio
```bash
git clone https://github.com/JoswardSilva/Proyecto-de-clima
cd Proyecto-de-clima
```

### 2. Configurar archivo `.env`
Crea un archivo `.env` basado en `.env.example`:

```
WEATHER_API_KEY=TU_API_KEY
TIDES_API_KEY=TU_API_KEY
CITY=Guanacaste,CR
LAT=10.417
LON=-85.917
TEMP_MAX=35
TEMP_MIN=15
```

> ⚠️ **Nunca subas `.env` a GitHub.**

### 3. Construir imagen Docker
```bash
docker build -t clima-app .
```

### 4. Ejecutar aplicación
```bash
docker run --rm -p 8501:8501 --env-file .env clima-app
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

### 2. Crear Secret con las API Keys
Debes crear las claves manualmente (no vienen en el repositorio):

```bash
kubectl create secret generic clima-secrets \
  --namespace application \
  --from-literal=WEATHER_API_KEY="<tu_api_key_de_openweather>" \
  --from-literal=TIDES_API_KEY="<tu_api_key_de_mareas>"
```

### 3. Verificar el Secret
```bash
kubectl get secret clima-secrets -n application -o yaml
```

### 4. Aplicar los manifiestos
```bash
kubectl apply -f configmap-clima.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 5. Verificar pods
```bash
kubectl get pods -A
```

### 6. Exponer servicios

Aplicación:
```bash
minikube service clima-app-service -n application
```
Grafana:
```bash
minikube service grafana-service -n application
```
Prometheus:
```bash
minikube service prometheus-service -n monitoring
```
Jaeger:
```bash
minikube service jaeger-service -n application
```
Para ejecutar todo el proceso de manera automatizada puedes utilizar los siguientes comandos:

```bash
./deploy.sh
```

y luego abrir los servicios con:

```bash
./open-services.sh
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
Incluye dashboards para:
- Uso de CPU
- Uso de CPU por Pod
- Estado del deployment `clima-app`
- Dashboards SRE (SLI/SLO/Error Budget)
- Alertas dinámicas

---

## Dependencias Python
```bash
pip install -r requirements.txt
```

---

## Seguridad
Este proyecto utiliza:
- **ConfigMaps** para configuraciones públicas.
- **Secrets** para variables sensibles.
- `.env.example` como plantilla SIN claves reales.

> ⚠️ No se deben subir API keys reales ni archivos `Secret` al repositorio.

---

## Autor
**Josward Silva**

