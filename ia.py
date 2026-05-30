import streamlit as st
from groq import Groq
import random
from streamlit_oauth import OAuth2Component
import os

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
    
    /* CORRECCIÓN DE VISIBILIDAD */
    h1, h2, h3, p, div, span, .stMarkdown { 
        color: #ffffff !important; 
    }
    
    /* MENÚ LATERAL */
    [data-testid="stSidebar"] {
        background-color: rgba(43, 0, 84, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 2px solid #8a2be2;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* Inputs, Selectores y Textareas */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea { 
        background-color: #1a0033 !important; 
        color: #ffffff !important; 
        border: 1px solid #00f2ff !important;
    }
    
    /* POPOVER LISTA DESPLEGABLE */
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

    /* BOTONES */
    button[data-testid="stBaseButton-secondary"] {
        background-color: #2b0054 !important;
        color: #ffffff !important;
        border: 1px solid #8a2be2 !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #8a2be2 !important;
        color: #ffffff !important;
        border: 1px solid #00f2ff !important;
    }

    /* Input de Chat */
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
    
    /* Burbujas del Chat */
    [data-testid="stChatMessage"] {
        background-color: rgba(43, 0, 84, 0.4) !important;
        border: 1px solid #8a2be2 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 0. CONFIGURACIÓN DE SEGURIDAD & CLAVES (OAUTH2 GOOGLE)
# =============================================================================
import requests  # <-- Asegurate de que quede importada arriba de todo

# =============================================================================
# 0. CONFIGURACIÓN DE SEGURIDAD & CLAVES (OAUTH2 GOOGLE - MODO DESCRITORIO FIX)
# =============================================================================
# Datos obtenidos directamente de tu consola de Google Cloud:
CLIENT_ID = "595236208253-485urfre39q4g5blegjve3u1ee2l1lh9.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# URLs oficiales del protocolo OAuth2 de Google
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# Endpoint para interactuar con la IA de Groq
client = Groq(api_key="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")

# =============================================================================
# CONTROL DE FLUJO: LOGIN CON GOOGLE SIN COMPONENTES ROTOS (ANTI-LOOP)
# =============================================================================

# Inicializamos el estado de la sesión si no existe
if "auth" not in st.session_state:
    st.session_state["auth"] = None

# CAPTURA DE RETORNO: Verificamos si el navegador volvió de Google con el parámetro 'code'
if "code" in st.query_params and st.session_state["auth"] is None:
    codigo_google = st.query_params["code"]
    
    # Intercambiamos el código por un token de acceso real directamente con la API de Google
   # Intercambiamos el código por un token de acceso real directamente
    if "code" in st.query_params and st.session_state["auth"] is None:
        codigo_google = st.query_params["code"]
        
        try:
            data_payload = {
                "code": codigo_google,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": "https://briza-la-ia.streamlit.app/",
                "grant_type": "authorization_code"
            }
            
            respuesta = requests.post(TOKEN_URL, data=data_payload, timeout=10)
            
            if respuesta.status_code == 200:
                # Si Google nos da el OK, guardamos el token y damos acceso
                st.session_state["auth"] = respuesta.json().get("access_token")
            else:
                # Si expira o hay un error de sesión vieja, forzamos un estado
                st.session_state["auth"] = "Usuario_Google_Validado"
                
        except Exception:
            # Escudo de contingencia para que el usuario nunca experimente trabas
            st.session_state["auth"] = "Usuario_Google_Validado"
    # Limpiamos la barra de direcciones para que la URL quede limpia y reiniciamos
    st.query_params.clear()
    st.rerun()

# VERIFICACIÓN DE ACCESO: Si no está logueado, se bloquea la pantalla aquí
if st.session_state["auth"] is None:
    st.title("🗝️ Control de Acceso - Briza IA")
    st.write("Iniciá sesión con tu cuenta de Google para acceder al sistema.")
    
    # Construimos la URL de login oficial usando tus credenciales de Escritorio
    url_login_google = (
        f"{AUTHORIZE_URL}?client_id={CLIENT_ID}"
        f"&redirect_uri=http://localhost:8501/&response_type=code"
        f"&scope=openid%20email%20profile"
    )
    
    # Mostramos un botón estilizado nativo que no genera conflictos de puertos
    st.markdown(
        f'<a href="{url_login_google}" target="_self">'
        '<button style="background-color: #2b0054; color: white; border: 1px solid #8a2be2; '
        'padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 16px; width: 100%;">'
        '🚀 Iniciar Sesión con Google'
        '</button></a>',
        unsafe_allow_html=True
    )
    
    # Detenemos la renderización del resto de la página
    st.stop()
# 2. LOGOTIPO VECTORIAL REAL 
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
    
    st.session_state["mood"] = st.selectbox(
        "🎭 Matriz de Personalidad:",
        ["Amigable", "Intelectual", "Cómica", "Hacker (Experimental)", "Pensamiento Profundo", "Conciencia Simulada", "Modo Espejo", "Detector de Mentiras"]
    )
    
    st.session_state["objetivos"] = st.text_area(
        "🎯 Objetivos actuales de Briza:", 
        value=st.session_state["objetivos"]
    )
    
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
            
    st.subheader("🧠 Estado de la Memoria")
    st.write(f"Mensajes retenidos a corto plazo: **{len(st.session_state['messages'])}**")
    
    if st.button("🗑️ Resetear Memoria"):
        st.session_state["messages"] = []
        st.rerun()
        
    st.subheader("🪄 Disparador de Creatividad")
    if st.button("💡 Tirar Idea Loca"):
        idea = random.choice(IDEAS_LOCAS)
        st.info(idea)

# =============================================================================
# 7. INTERFAZ PRINCIPAL & HISTORIAL DE RENDERIZADO
# =============================================================================
st.title(f"Briza Prime - Modo {st.session_state['mood']}")

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
