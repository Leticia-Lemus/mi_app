# pip install streamlit

import streamlit as st
import pandas as pd
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
###
st.title("📊 Mi primera App")
st.caption("Haz preguntas sobre la tabla de diabetes")

##cargar bd-----------------

# Puedes usar tu propio archivo aquí
df = pd.read_csv("diabetes.csv")
st.dataframe(df)

#Dataframe a texto
def dataframe_a_contexto(df):
    return df.to_csv(index=False)


# Función para generar respuesta con OpenAI
def responder_pregunta(pregunta, contexto_tabla):
    sistema = (
        "Eres un asistente que responde únicamente con base en la siguiente tabla de datos.\n"
        "Si la pregunta no se relaciona con la tabla, responde: 'Lo siento, solo puedo responder preguntas relacionadas con los datos mostrados.'\n\n"
        "Tabla de datos:\n"
        f"{contexto_tabla}"
    )

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": pregunta}
            ],
            temperature=0
        )
        return respuesta["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"


pregunta = st.chat_input("Haz una pregunta sobre la tabla...")
if pregunta:
    st.write(f"**Tú:** {pregunta}")
    contexto = dataframe_a_contexto(df)
    respuesta = responder_pregunta(pregunta, contexto)
    st.write(f"**Chatbot:** {respuesta}")

# Pick a number using a slider
#number = st.slider("Elige un número", 0, 100)

# Plotear el sin(number)
#import numpy as np
#import matplotlib.pyplot as plt
##x = np.linspace(0, 10, 100)
#y = np.sin(x + number)
#plt.plot(x, y)
#st.pyplot(plt)

# ls -> enlista documentos
# cd -> cambia de directorio

# stremlit run pruebaSt.py

#activar el entorno .venv: .venv\Scripts\activate
