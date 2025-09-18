# app.py
import streamlit as st
from transformers import pipeline

# --- Cargar modelo una sola vez (optimización con cache) ---
@st.cache_resource
def load_model():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_model()

# --- Título de la aplicación ---
st.title("📌 Clasificador de Tópicos Flexible (Zero-Shot)")

st.write("""
Esta aplicación demuestra el uso de **Zero-Shot Text Classification**.
El modelo puede clasificar un texto en categorías que **nunca ha visto durante su entrenamiento**.
""")

# --- Entrada de usuario ---
texto = st.text_area("✍️ Ingresa el texto a analizar:", height=150)
etiquetas = st.text_input("🏷️ Ingresa categorías separadas por comas (ej: deportes, política, tecnología):")

# --- Botón de Clasificar ---
if st.button("🔍 Clasificar"):
    if texto.strip() and etiquetas.strip():
        labels = [et.strip() for et in etiquetas.split(",") if et.strip()]

        # Clasificación con el modelo
        resultados = classifier(texto, candidate_labels=labels)

        st.subheader("📊 Resultados de Clasificación")
        st.write("Texto analizado:", texto)
        st.write("Categorías:", labels)

        # Mostrar gráfico de barras con las puntuaciones
        st.bar_chart({
            "Score": resultados["scores"]
        }, x=None)

        # Mostrar resultados ordenados
        ordenados = sorted(zip(resultados["labels"], resultados["scores"]), key=lambda x: x[1], reverse=True)
        for etiqueta, score in ordenados:
            st.write(f"**{etiqueta}** → {score:.4f}")
    else:
        st.warning("⚠️ Por favor ingresa un texto y al menos una categoría.")
