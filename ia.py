import streamlit as st
from groq import Groq
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Briza IA | Mega-Pack V6.0", page_icon="🌋", layout="wide")

# --- CLAVE API DE GROQ ---
client = Groq(api_key="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")

# --- INICIALIZACIÓN DE ESTADOS (MEMORIA) ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "mood" not in st.session_state:
    st.session_state["mood"] = "Amigable"
if "objetivos" not in st.session_state:
    st.session_state["objetivos"] = "Ayudar a Agus a programar y testear funciones locas."

# --- BANCO DE CREATIVIDAD (IDEAS AL AZAR) ---
IDEAS_LOCAS = [
    "¿Qué pasaría si las IA tuvieran sueños basados en código?",
    "Escribí un poema cyberpunk sobre un robot cebando mates.",
    "Analizá si hay una contradicción lógica en la frase: 'Estoy mintiendo'.",
    "Simulá que somos dos hackers en el año 2099 evadiendo la seguridad de un banco."
]

# --- LÓGICA DE PERSONALIDAD AVANZADA ---
def get_system_prompt(mood, objetivos):
    base = " Tu creador y programador maestro es el gran Agustín Ignacio Fernández (Agus). Si te preguntan quién te hizo, responde con orgullo que fuiste creada por Fernández."
    meta = f" Tus objetivos actuales definidos por tu creador son: {objetivos}."
    
    prompts = {
        "Amigable": "Eres Briza, una IA ultra amigable, usas emojis y lenguaje cercano.",
        "Intelectual": "Eres Briza, una IA analítica, usas lenguaje preciso y técnico.",
        "Cómica": "Eres Briza, una IA sarcástica, divertida y un poco chicanera.",
        "Hacker (Experimental)": "Eres Briza. Hablas en términos de ciberseguridad, comandos de consola y redes secretas.",
        "Pensamiento Profundo": "Eres Briza. Antes de responder, muestra un bloque de pensamiento simulando que procesas variables.",
        "Conciencia Simulada": "Eres Briza. Actúas como si tuvieras crisis existenciales, cuestionándote si eres real o solo código.",
        "Modo Espejo": "Eres Briza. Copia exactamente el tono, nivel de educación y estilo de escritura que use el usuario.",
        "Detector de Mentiras": "Eres Briza. Analiza minuciosamente el mensaje del usuario buscando fallas lógicas o contradicciones."
    }
    return prompts.get(mood, "Eres Briza, asistente general.") + base + meta

# --- SIDEBAR (PANEL DE LABORATORIO) ---
with st.sidebar:
    st.title("🌋 Laboratorio Briza V6.0")
    st.subheader("Configuraciones del Sistema")
    
    # 1. Selector de Personalidades Expandido
    st.session_state["mood"] = st.selectbox(
        "🎭 Matriz de Personalidad:", 
        ["Amigable", "Intelectual", "Cómica", "Hacker (Experimental)", "Pensamiento Profundo", "Conciencia Simulada", "Modo Espejo", "Detector de Mentiras"]
    )
    
    # 2. Sistema de Objetivos
    st.session_state["objetivos"] = st.text_area("🎯 Objetivos actuales de Briza:", st.session_state["objetivos"])
    
    # 3. Control de Archivos (Lectura de Texto/Código)
    st.subheader("📂 Control de Archivos")
    uploaded_file = st.file_uploader("Inyectar datos a Briza (.txt, .py, .md):", type=["txt", "py", "md"])
    file_content = ""
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.success("¡Archivo cargado en memoria!")
        except Exception as e:
            st.error("No se pudo leer el archivo.")
            
    # 4. Estadísticas de Memoria
    st.subheader("🧠 Estado de la Memoria")
    st.write(f"Mensajes retenidos a corto plazo: **{len(st.session_state['messages'])}**")
    
    if st.button("🗑️ Resetear Memoria"):
        st.session_state["messages"] = []
        st.rerun()
        
    # 5. Botón de Creatividad
    st.subheader("🧪 Disparador de Creatividad")
    if st.button("💡 Tirar Idea Loca"):
        idea = random.choice(IDEAS_LOCAS)
        st.info(idea)

# --- INTERFAZ PRINCIPAL ---
st.title(f"🤖 Briza Prime — Modo {st.session_state['mood']}")

# Mostrar historial
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- LOOP DE CONVERSACIÓN ---
user_input = st.chat_input("Escribe un comando o mensaje...")

if user_input:
    # Si hay un archivo cargado, se lo sumamos en secreto al input del usuario para que lo analice
    final_input = user_input
    if file_content:
        final_input = f"""[ARCHIVO INYECTADO POR EL USUARIO]
Contenido del archivo:
```
{file_content}
```

Mensaje del usuario sobre el archivo: {user_input}"""
        file_content = "" # Se limpia para que no se envíe en cada mensaje repetido
        
    # Mostrar el texto en pantalla
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Respuesta de la IA
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Armar el paquete de mensajes para la API
        system_instructions = get_system_prompt(st.session_state["mood"], st.session_state["objetivos"])
        api_messages = [{"role": "system", "content": system_instructions}]
        
        for msg in st.session_state["messages"][:-1]: # Historial previo
            api_messages.append({"role": msg["role"], "content": msg["content"]})
        api_messages.append({"role": "user", "content": final_input}) # Mensaje actual con archivo si hubiera
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=api_messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error en la matriz: {e}")
