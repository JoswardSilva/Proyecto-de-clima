import requests
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import matplotlib.dates as mdates
import time
from dotenv import load_dotenv
load_dotenv()
import os
# ------------OPENTELEMETRY------------
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Configure tracer
resource = Resource.create({"service.name": "clima-app"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter(
    endpoint="http://otel-collector.opentelemetry.svc.cluster.local:4317",
    insecure=True
)

provider.add_span_processor(BatchSpanProcessor(exporter))

# Auto-instrument requests
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

# ------------APP SETTINGS------------
st.set_page_config(page_title="Clima y Mareas", layout="centered")

CITY = "Guanacaste,CR"
LAT = 10.417
LON = -85.917


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
TIDES_API_KEY = os.getenv("TIDES_API_KEY", "")

TEMP_MAX = int(os.getenv("TEMP_MAX", 35))
TEMP_MIN = int(os.getenv("TEMP_MIN", 15))

CITY = os.getenv("CITY", "San Jose")
LAT = os.getenv("LAT", "9.9281")
LON = os.getenv("LON", "-84.0907")

WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
TIDES_URL   = f"https://www.worldtides.info/api/v3?heights&lat={LAT}&lon={LON}&key={TIDES_API_KEY}"

# ------------FUNCIONES------------
def get_weather():
    with tracer.start_as_current_span("get_weather"):
        r = requests.get(WEATHER_URL)
        data = r.json()

        if r.status_code != 200:
            st.error(f"Error al obtener clima: {data.get('message')}")
            return None
        
        return {
            "temperatura": data["main"]["temp"],
            "humedad": data["main"]["humidity"],
            "presion": data["main"]["pressure"],
        }

def get_tides():
    with tracer.start_as_current_span("get_tides"):
        r = requests.get(TIDES_URL)
        #st.write("DEBUG respuesta mareas:", r.text)
        data = r.json()

        if "heights" not in data:
            st.error("Error al obtener mareas")
            return None
        
        return data["heights"]

# ------------UI------------
with tracer.start_as_current_span("render_ui"):

    st.title("🌤️ Tracker de Clima y Mareas")
    st.write(f"📍 Ciudad: **{CITY}**")

    weather = get_weather()

    if weather:
        st.metric("🌡️ Temperatura", f"{weather['temperatura']} °C")
        st.metric("💧 Humedad", f"{weather['humedad']} %")
        st.metric("⬇️ Presión", f"{weather['presion']} hPa")

        if weather["temperatura"] > TEMP_MAX:
            st.error(f"🔥 ALERTA: Temperatura muy alta ({weather['temperatura']}°C)")
        elif weather["temperatura"] < TEMP_MIN:
            st.warning(f"❄️ ALERTA: Temperatura muy baja ({weather['temperatura']}°C)")
        else:
            st.success("✅ Temperatura dentro del rango normal.")

    tides = get_tides()

    if tides:
        st.subheader("🌊 Mareas próximas (Gráfico)")

        times_utc = [datetime.fromisoformat(t["date"]) for t in tides]
        cr_tz = pytz.timezone("America/Costa_Rica")
        times = [t.replace(tzinfo=pytz.UTC).astimezone(cr_tz) for t in times_utc]
        heights = [t["height"] for t in tides]

        plt.figure(figsize=(10, 4))
        plt.plot(times, heights, marker='o', linestyle='-', alpha=0.7)

        max_idx = heights.index(max(heights))
        min_idx = heights.index(min(heights))

        plt.scatter(times[max_idx], heights[max_idx], color='red', s=100, label='Marea Alta')
        plt.scatter(times[min_idx], heights[min_idx], color='blue', s=100, label='Marea Baja')

        plt.title("Altura de la marea")
        plt.xlabel("Hora")
        plt.ylabel("Altura (m)")
        plt.grid(True)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M', tz=cr_tz))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)

        st.pyplot(plt)


# Auto-refresh cada minuto


