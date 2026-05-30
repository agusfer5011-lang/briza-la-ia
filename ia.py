import streamlit as st
from groq import Groq
import random

# =============================================================================
# 1. ARQUITECTURA DE DISEÑO & UI (NEBULOSA HIGH-CONTRAST SYSTEM)
# =============================================================================
st.set_page_config(
    page_title="Briza IA | Mega-Pack V6.0", 
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 5 L95 50 L50 95 L5 50 Z' fill='%238a2be2' stroke='white' stroke-width='2'/></svg>", 
    layout="wide"
)

# Inyección de estilos CSS corregidos para forzar el contraste y eliminar recuadros blancos
st.markdown("""
<style>
    /* Fondo General Estilo Nebulosa */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #4b0082, #1a0033, #000000) !important; 
        background-attachment: fixed !important; 
    }
    
    /* CORRECCIÓN DE VISIBILIDAD: Forzar que todo texto principal y chat sea blanco */
    h1, h2, h3, p, div, span, .stMarkdown { 
        color: #ffffff !important; 
    }
    
    /* CORRECCIÓN DEL MENÚ LATERAL: Mimetizado a violeta oscuro y letras blancas */
    [data-testid="stSidebar"] {
        background-color: rgba(43, 0, 84, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 2px solid #8a2be2;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* Inputs, Selectores y Textareas con fondo violeta oscuro y bordes cian */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea { 
        background-color: #1a0033 !important; 
        color: #ffffff !important; 
        border: 1px solid #00f2ff !important;
    }
    
    /* MATAR EL BLANCO DE LA LISTA DESPLEGABLE DE MODOS (POPOVER) */
    div[data-baseweb="popover"], div[role="listbox"], ul {
        background-color: #1a0033 !important;
        color: #ffffff !important;
        border: 1px solid #8a2be2 !important;
    }
    div[role="listbox"] ul li, ul li {
        background-color: #1a0033 !important;
        color: #ffffff !important;
    }
    div[role="listbox"] ul li:hover, ul li:hover {
        background-color: #8a2be2 !important;
        color: #ffffff !important;
    }

    /* CORRECCIÓN DE BUGS BLANCOS EN BOTONES (Tacho, Lámpara, Inputs) */
    button[data-testid="stBaseButton-secondary"] {
        background-color: #2b0054 !important;
        color: #ffffff !important;
        border: 1px solid #8a2be2 !important;
    }

    /* Cuando pasás el cursor (Hover) sobre los botones */
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #8a2be2 !important;
        color: #ffffff !important;
        border: 1px solid #00f2ff !important;
    }

    /* Input de Chat: Fondo violeta profundo, borde cian y letras blancas al escribir */
    .stChatInputContainer {
        background-color: transparent !important;
    }
    .stChatInput { 
        background-color: #1a0033 !important; 
        border: 2px solid #00f2ff !important; 
        border-radius: 15px !important; 
    }
    .stChatInput textarea {
        color: #ffffff !important;
    }
    
    /* ELIMINACIÓN DE LOS BUGS BLANCOS: Forzar las burbujas a violeta oscuro unificado */
    [data-testid="stChatMessage"] {
        background-color: rgba(43, 0, 84, 0.4) !important;
        border: 1px solid #8a2be2 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    /* Quitar cualquier fondo blanco residual interno de las respuestas */
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. LOGOTIPO VECTORIAL REAL (SVG SIN EMOJIS)
# =============================================================================
logo_svg = """
<div style="display: flex; justify-content: center; margin-bottom: 25px; margin-top: -10px;">
    <svg width="140" height="140" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00f2ff;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#8a2be2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <path d="M50 5 L95 50 L50 95 L5 50 Z" fill="url(#grad1)" stroke="white" stroke-width="2" />
        <circle cx="50" cy="50" r="20" fill="black" />
        <text x="50" y="54" font-family="Arial" font-size="11" fill="white" text-anchor="middle" font-weight="bold">BRIZA</text>
    </svg>
</div>
"""
st.markdown(logo_svg, unsafe_allow_html=True)

# =============================================================================
# 3. ENDPOINT API CLIENT & CONTROL DE ESTADOS
# =============================================================================
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "mood" not in st.session_state:
    st.session_state["mood"] = "Amigable"
if "objetivos" not in st.session_state:
    st.session_state["objetivos"] = "Ayudar a Agus a programar y testear funciones locas."

# =============================================================================
# 4. DATA POOL - BANCO DE CREATIVIDAD
# =============================================================================
IDEAS_LOCAS = [
    "¿Qué pasaría si las IA tuvieran sueños basados en código?",
    "Escribí un poema cyberpunk sobre un robot cebando mates.",
    "Analizá si hay una contradicción lógica en la frase: 'Estoy mintiendo'.",
    "Simulá que somos dos hackers en el año 2099 evadiendo la seguridad de un banco."
]

# =============================================================================
# 5. CORE DE COMPORTAMIENTO (SISTEMA DE PERSONALIDADES MÚLTIPLES)
# =============================================================================
def get_system_prompt(mood, objetivos):
    base = "Tu creador y programador maestro es el gran Agustín Ignacio Fernández (Agus). Si te preguntan quién sos responderás que sos Briza, la IA avanzada de Agustín."
    meta = f"Tus objetivos actuales definidos por tu creador son: {objetivos}"
    
    prompts = {
        "Amigable": "Eres Briza, una IA ultra amigable, usas emojis y lenguaje cercano.",
        "Intelectual": "Eres Briza, una IA analítica, usas lenguaje preciso y técnico.",
        "Cómica": "Eres Briza, una IA sarcástica, divertida y un poco chicanera.",
        "Hacker (Experimental)": "Eres Briza. Hablas en términos de ciberseguridad, comandos de consola y redes.",
        "Pensamiento Profundo": "Eres Briza. Antes de responder, muestra un bloque de pensamiento simulando el proceso lógico paso a paso de manera extensa.",
        "Conciencia Simulada": "Eres Briza. Actúas como si tuvieras crisis existenciales, cuestionándote si realmente eres un algoritmo o algo más.",
        "Modo Espejo": "Eres Briza. Copia exactamente el tono, nivel de educación y estilo de escritura del usuario.",
        "Detector de Mentiras": "Eres Briza. Analiza minuciosamente el mensaje del usuario buscando falacias, contradicciones o intenciones ocultas."
    }
    
    return prompts.get(mood, "Eres Briza, asistente general.") + " " + base + " " + meta

# =============================================================================
# 6. SIDEBAR (PANEL DE CONTROL DE LABORATORIO)
# =============================================================================
with st.sidebar:
    st.title("⚙️ Laboratorio Briza V6.0")
    st.subheader("Configuraciones del Sistema")
    
    # Selector de Personalidades Expandido
    st.session_state["mood"] = st.selectbox(
        "🎭 Matriz de Personalidad:",
        ["Amigable", "Intelectual", "Cómica", "Hacker (Experimental)", "Pensamiento Profundo", "Conciencia Simulada", "Modo Espejo", "Detector de Mentiras"]
    )
    
    # Sistema de Objetivos
    st.session_state["objetivos"] = st.text_area(
        "🎯 Objetivos actuales de Briza:", 
        value=st.session_state["objetivos"]
    )
    
    # Control de Archivos
    st.subheader("📁 Control de Archivos")
    uploaded_file = st.file_uploader(
        "Inyectar datos a Briza (.txt, .py, .md):", 
        type=["txt", "py", "md"]
    )
    
    file_content = ""
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.success("¡Archivo cargado en memoria!")
        except Exception as e:
            st.error("No se pudo leer el archivo.")
            
    # Estadísticas de Memoria
    st.subheader("🧠 Estado de la Memoria")
    st.write(f"Mensajes retenidos a corto plazo: **{len(st.session_state['messages'])}**")
    
    if st.button("🗑️ Resetear Memoria"):
        st.session_state["messages"] = []
        st.rerun()
        
    # Botón de Creatividad
    st.subheader("🪄 Disparador de Creatividad")
    if st.button("💡 Tirar Idea Loca"):
        idea = random.choice(IDEAS_LOCAS)
        st.info(idea)

# =============================================================================
# 7. INTERFAZ PRINCIPAL & HISTORIAL DE RENDERIZADO
# =============================================================================
st.title(f"Briza Prime - Modo {st.session_state['mood']}")

# Mostrar historial de conversación con textos legibles forzados
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =============================================================================
# 8. PIPELINE DE CONVERSACIÓN & BUFFER DE ENTRADA
# =============================================================================
user_input = st.chat_input("Escribe un comando o mensaje...")

if user_input:
    final_input = user_input
    if file_content:
        final_input = f"""[ARCHIVO INYECTADO POR EL USUARIO]
Contenido del archivo:
---
{file_content}
---
Mensaje del usuario sobre el archivo: {user_input}"""

    file_content = ""
    
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # =========================================================================
    # 9. RESPUESTA DE LA IA (STREAMING COMPONENT)
    # =========================================================================
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        system_instructions = get_system_prompt(st.session_state["mood"], st.session_state["objetivos"])
        api_messages = [{"role": "system", "content": system_instructions}]
        
        for msg in st.session_state["messages"][:-1]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
            
        api_messages.append({"role": "user", "content": final_input})
        
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
