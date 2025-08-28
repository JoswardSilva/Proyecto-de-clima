import requests
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import matplotlib.dates as mdates

# 🔑 API Keys
WEATHER_API_KEY = "6003055f360057221483472cfe44db29"
TIDES_API_KEY = "0d6fe98a-946e-4526-8228-78a2869019a2"

# Ciudad y coordenadas
CITY = "Guanacaste,CR"
LAT = 10.417 #9.9333    # latitud
LON = -85.917#84.0833  # longitud

# Umbrales
TEMP_MAX = 35
TEMP_MIN = 15

# URLs
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
TIDES_URL = f"https://www.worldtides.info/api/v3?heights&lat={LAT}&lon={LON}&key={TIDES_API_KEY}"

def get_weather():
    response = requests.get(WEATHER_URL)
    data = response.json()
    if response.status_code != 200:
        st.error(f"Error al obtener datos: {data.get('message')}")
        return None
    return {
        "temperatura": data["main"]["temp"],
        "humedad": data["main"]["humidity"],
        "presion": data["main"]["pressure"]
    }

def get_tides():
    response = requests.get(TIDES_URL)
    data = response.json()
    if "heights" not in data:
        st.error("Error al obtener datos de mareas")
        return None
    return data["heights"]

# ---- Interfaz Streamlit ----
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

# ---- Mareas con gráfico ----
tides = get_tides()
if tides:
    st.subheader("🌊 Mareas próximas (Gráfico)")

    # Preparar datos para graficar Convertir hora a Costa Rica
    times_utc = [datetime.fromisoformat(t["date"]) for t in tides]
    cr_tz = pytz.timezone("America/Costa_Rica")
    times = [t.replace(tzinfo=pytz.UTC).astimezone(cr_tz) for t in times_utc]
    heights = [t["height"] for t in tides]
   # times = [datetime.fromisoformat(t["date"]) for t in tides]
   #heights = [t["height"] for t in tides]

    plt.figure(figsize=(10,4))
    plt.plot(times, heights, marker='o', linestyle='-', color='gray', alpha=0.6)

 # Encontrar índice de marea alta y baja
    max_idx = heights.index(max(heights))
    min_idx = heights.index(min(heights))
# Marcar marea alta en rojo
    plt.scatter(times[max_idx], heights[max_idx], color='red', s=100, label='Marea Alta')
# Marcar marea baja en azul
    plt.scatter(times[min_idx], heights[min_idx], color='blue', s=100, label='Marea Baja')
# Relleno del área bajo la curva
    plt.fill_between(times, heights, color='lightblue', alpha=0.2)


    plt.fill_between(times, heights, color='lightblue', alpha=0.3)
    plt.title("Altura de la marea")
    plt.xlabel("Hora")
    plt.ylabel("Altura (m)")
    plt.xticks(rotation=45)
    plt.grid(True)

# Formato de fecha y hora 
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M', tz=cr_tz))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    st.pyplot(plt)
