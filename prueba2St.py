from openai import OpenAI
import streamlit as st
import pandas as pd

# === Sidebar ===
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# === Cargar la base de datos ===
try:
    df = pd.read_csv("diabetes.csv")
    st.session_state["diabetes_data"] = df
    st.sidebar.success("Base de datos diabetes.csv cargada correctamente.")
except FileNotFoundError:
    st.sidebar.error("Archivo diabetes.csv no encontrado.")
    st.stop()

# === Interfaz principal ===
st.title("💬 Chatbot de diabetes")
st.caption("🤖 Este bot solo responde preguntas basadas en la base de datos diabetes.csv")
st.write("Vista previa de los datos:")
st.dataframe(st.session_state["diabetes_data"].head())

# === Definir instrucciones del sistema ===
columnas = ", ".join(df.columns)
contexto = f"""Este asistente que responde exclusivamente preguntas relacionadas con la base de datos de pacientes con diabetes.
Los nombres de las columnas son: {columnas}.
Solo puedes usar información contenida en esta tabla. Si la pregunta no se relaciona con estos datos, responde:
"Lo siento, solo puedo responder preguntas relacionadas con la información de la base de datos diabetes."
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": contexto},
        {"role": "assistant", "content": "¿En qué puedo ayudarte con los datos de diabetes?"}
    ]

# === Mostrar el historial de mensajes ===
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# === Procesar input del usuario ===
if prompt := st.chat_input("Haz una pregunta sobre los datos..."):
    if not openai_api_key:
        st.info("Por favor, ingresa tu API key de OpenAI.")
        st.stop()

    # Guardar la pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Llamar a OpenAI
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content

    # Mostrar la respuesta y guardarla
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
