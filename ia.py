import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pandas as pd

# --- 1. CONFIGURACIÓN DEL SISTEMA ---
st.set_page_config(page_title="Brisa IA | Ultimate Suite", page_icon="🚀", layout="wide")

# --- 2. MOTOR CORE (HARDCODED PARA ESTABILIDAD) ---
client = Groq(api_key="gsk_Xre2owlZBcX8Zq3BdV8tWGdyb3FYJdjiyv9ty24jrSEuVJsTqpQ")

# --- 3. ESTADOS DE SESIÓN (EL CEREBRO) ---
if "messages" not in st.session_state: st.session_state["messages"] = []
if "mood" not in st.session_state: st.session_state["mood"] = "Amigable"
if "token_count" not in st.session_state: st.session_state["token_count"] = 0
if "start_time" not in st.session_state: st.session_state["start_time"] = datetime.now()

# --- 4. LÓGICA DE PERSONALIDADES ---
def get_system_prompt(mood):
    prompts = {
        "Amigable": "Eres Brisa, una IA ultra amigable, usas emojis y lenguaje cercano.",
        "Intelectual": "Eres Brisa, una IA analítica, usas terminología científica y profunda.",
        "Cómica": "Eres Brisa, una IA sarcástica y divertida. Nunca te tomas nada en serio.",
        "Motivadora": "Eres Brisa, una coach de vida. Empoderas al usuario en cada respuesta."
    }
    return prompts.get(mood, "Eres Brisa, asistente general.")

# --- 5. SIDEBAR SUPERCOMPLETO ---
with st.sidebar:
    st.header("🚀 Brisa IA Control")
    st.session_state["mood"] = st.selectbox("Personalidad:", ["Amigable", "Intelectual", "Cómica", "Motivadora"])
    
    st.markdown("### 📊 Estadísticas")
    st.metric("Tokens Consumidos", st.session_state["token_count"])
    st.metric("Tiempo de sesión", f"{(datetime.now() - st.session_state['start_time']).seconds // 60} min")
    
    st.markdown("---")
    if st.button("🧨 BORRAR TODO EL HISTORIAL"):
        st.session_state["messages"] = []
        st.session_state["token_count"] = 0
        st.rerun()

# --- 6. INTERFAZ Y LOGICA DE CHAT ---
st.title(f"Brisa IA v4.0 - Modo: {st.session_state['mood']}")
st.markdown("La IA más avanzada, sin configuraciones molestas.")

# Mostrar chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. MOTOR DE RESPUESTA CON STREAMING AVANZADO ---
if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Historial formateado
        system_msg = {"role": "system", "content": get_system_prompt(st.session_state["mood"])}
        
        stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[system_msg] + st.session_state["messages"],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")
        
        placeholder.markdown(full_response)
        st.session_state["token_count"] += len(full_response) // 4
    
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# --- 8. FUNCIONES EXTRAS CHULAS ---
with st.expander("🛠️ Herramientas Pro"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Estado: OPERATIVO")
        st.info("Brisa está usando la API de Groq con Llama 3.")
    with col2:
        st.write("Exportar datos:")
        st.download_button("Descargar registro JSON", str(st.session_state["messages"]), "historial.json")

# --- 9. PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado para Brisa IA | © 2026")
        

