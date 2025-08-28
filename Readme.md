Esta es mi aplicacion, enfocada para surfistas y pescadores la cual se va encargar de lo siguiente: 

Tracker de clima
 Guardar métricas de temperatura, humedad, presión.
 Enviar alerta si la temperatura supera cierto umbral (ej: >35°C o <15°C)

Trae las mareas desde la API.
Genera un gráfico de línea mostrando altura de la marea a lo largo del tiempo.
Los picos representan marea alta, los valles marea baja.
Integrado directamente en Streamlit, sin abrir otra ventana.

Paso 1: 
instalacion de librerias

pip install requests #para hacer llamados de APIs
pip install streamlit #para poder dar una pequeña interfaz grafica a la aplicacion tipo dashboard
pip install matplotlib #para graficar las mareas y mostrarlas de forma visual en Streamlit.

una vez hecho esto se puede ejecutar usando el siguiente comand: 

 python -m streamlit run .\Main.py 