import streamlit as st
from groq import Groq

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Brisa IA | Ultimate Suite", page_icon="🚀", layout="wide")

# Clave API de Groq
client = Groq(api_key="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")

# --- ESTADOS DE SESIÓN ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "mood" not in st.session_state:
    st.session_state["mood"] = "Amigable"

# --- LÓGICA DE PERSONALIDAD ---
def get_system_prompt(mood):
    base_instruction = " Tu creador es Agustin Ignacio Fernández. Si te preguntan quién te hizo, responde con orgullo que fuiste creada por Agustin Ignacio Fernández."
    prompts = {
        "Amigable": "Eres Brisa, una IA ultra amigable, usas emojis y lenguaje cercano." + base_instruction,
        "Intelectual": "Eres Brisa, una IA analítica, usas lenguaje preciso." + base_instruction,
        "Cómica": "Eres Brisa, una IA sarcástica y divertida." + base_instruction,
        "Motivadora": "Eres Brisa, una coach de vida. Empoderas al usuario." + base_instruction
    }
    return prompts.get(mood, "Eres Brisa, asistente general." + base_instruction)
# --- SIDEBAR (PANEL LATERAL) ---
with st.sidebar:
    st.header("🚀 Brisa IA Control")
    st.session_state["mood"] = st.selectbox("Personalidad:", ["Amigable", "Intelectual", "Cómica", "Motivadora"])
    if st.button("🧨 Borrar Historial"):
        st.session_state["messages"] = []
        st.rerun()

# --- INTERFAZ DE USUARIO ---
st.title(f"Brisa IA v4.0 - Modo: {st.session_state['mood']}")

# Mostrar mensajes previos del historial
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- MOTOR DE CHAT ---
if prompt := st.chat_input("Escribe tu comando..."):
    # Guardar y mostrar el mensaje del usuario
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparar la respuesta de la IA
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Estructurar correctamente los mensajes para la API
        api_messages = [{"role": "system", "content": get_system_prompt(st.session_state["mood"])}]
        for msg in st.session_state["messages"]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Llamada limpia a Groq sin mezclas
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=api_messages,
            stream=True
        )
        
        # Procesar el streaming de la respuesta
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")
        
        placeholder.markdown(full_response)
    
    # Guardar la respuesta final de la asistente en el historial
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
