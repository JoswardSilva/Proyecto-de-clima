# Usar imagen oficial de Python
FROM python:3.11-slim

# Evitar prompts de interacción
ENV DEBIAN_FRONTEND=noninteractive

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para matplotlib y streamlit
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar el archivo principal
COPY Main.py .

# Instalar dependencias de Python directamente
RUN pip install --no-cache-dir \
    streamlit \
    requests \
    matplotlib \
    pytz \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-requests


# Exponer el puerto por defecto de Streamlit
EXPOSE 8501

# Comando por defecto para correr la app
CMD ["streamlit", "run", "Main.py", "--server.port=8501", "--server.address=0.0.0.0"]
