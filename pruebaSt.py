from openai import OpenAI
import streamlit as st
import pandas as pd

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

##Lectura de la base de datos
try:
    df = pd.read_csv("diabetes.csv")  
    st.session_state["diabetes_data"] = df  # Guarda el DataFrame en la sesión
    st.sidebar.success("Base de datos diabetes.csv cargada correctamente.")
except FileNotFoundError:
    st.sidebar.error("Archivo diabetes.csv no encontrado.")


# Interfaz
st.title("Chatbot con una base de datos de diabetes")
st.write("Datos cargados:")
#st.dataframe(df)
if "diabetes_data" in st.session_state:
    st.dataframe(st.session_state["diabetes_data"])


#st.title("💬 Chatbot")
#st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    #st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
     st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "Este es un asistente que solo puede responder preguntas sobre los datos de la base diabetes.csv. "
                "Si la pregunta no está relacionada, responde: "
                "'Lo siento, solo puedo responder preguntas relacionadas con la información de la base de datos diabetes.'"
            )
        },
        {
            "role": "assistant",
            "content": "¿En qué puedo ayudarte con los datos de diabetes?"
        }
    ]


#Mostrar historial de conversación
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
#procesar pregunta
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
 # === Filtro previo: solo permitir temas relacionados con diabetes ===
    allowed_terms = [
        "glucosa", "edad", "insulina", "presión", "imc", "embarazo",
        "piel", "pedigree", "diabetes", "resultado", "pacientes"
    ]
    if not any(term in prompt.lower() for term in allowed_terms):
        msg = "Lo siento, solo puedo responder preguntas relacionadas con la información de la base de datos diabetes."
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        st.stop()
    #enviar al modelo si pasa el filtro
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

