# app.py
import streamlit as st
from groq import Groq

# --- Ingreso de API Key ---
st.title("🤖 Chatbot Conversacional con Memoria")
st.write("Este chatbot usa **llama3-8b-8192** vía la API de **Groq**.")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Input seguro para la clave
api_key_input = st.text_input("🔑 Ingresa tu API Key de Groq:", type="password")

if api_key_input:
    st.session_state.api_key = api_key_input

# Si no hay clave, pedimos al usuario que la ingrese
if not st.session_state.api_key:
    st.warning("Por favor ingresa tu API Key para continuar.")
    st.stop()

# --- Cliente de Groq con la clave ingresada ---
client = Groq(api_key=st.session_state.api_key)

# --- Inicializar historial en session_state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Mostrar historial de la conversación ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Entrada del usuario ---
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar al modelo con todo el historial
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
)


        respuesta_bot = response.choices[0].message.content

        # Guardar respuesta del bot
        st.session_state.messages.append({"role": "assistant", "content": respuesta_bot})

        with st.chat_message("assistant"):
            st.markdown(respuesta_bot)

    except Exception as e:
        st.error(f"⚠️ Error en la llamada a la API: {e}")
