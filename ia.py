import streamlit as st
import os
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
from groq import Groq

# 1. Configuración de página
st.set_page_config(page_title="brisa ai", page_icon="🤖")

# 2. Cargar configuraciones del .env
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 3. Configurar OAuth
oauth = OAuth2Component(
    GOOGLE_CLIENT_ID, 
    GOOGLE_CLIENT_SECRET, 
    "https://accounts.google.com/o/oauth2/v2/auth", 
    "https://oauth2.googleapis.com/token", 
    "https://oauth2.googleapis.com/revoke"
)

# 4. Lógica de Login con persistencia
if "auth_token" not in st.session_state:
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #111111 100%); color: white; }
        .login-box { text-align: center; padding-top: 100px; }
        </style>
        <div class="login-box">
            <h1>🤖 Brisa IA</h1>
            <p>Inicia sesión con Google para comenzar</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        result = oauth.authorize_button(
            name="Iniciar sesión con Google",
            icon="https://www.google.com/favicon.ico",
            redirect_uri="https://briza-la-ia.streamlit.app",
            scope="openid email profile",
        )
        if result:
            st.session_state["auth_token"] = result
            st.rerun()
    st.stop()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        result = oauth.authorize_button(
            name="Iniciar sesión con Google",
            icon="https://www.google.com/favicon.ico",
            redirect_uri="https://briza-la-ia.streamlit.app",
            scope="openid email profile",
        )
        if result:
            st.session_state["auth_token"] = result
            st.rerun()
    st.stop()

# --- A PARTIR DE ACÁ VA TU CÓDIGO ORIGINAL ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# (A partir de acá mantené el resto de tu código tal cual lo tenías: los estados, el chat, etc.)
if "lista_chats" not in st.session_state:
    st.session_state["lista_chats"] = {"Chat 1": []}

if "chat_actual" not in st.session_state:
    st.session_state["chat_actual"] = "Chat 1"

if st.session_state["chat_actual"] not in st.session_state["lista_chats"]:
    st.session_state["lista_chats"][st.session_state["chat_actual"]] = []

# --- INYECCIÓN DE ESTILOS AVANZADOS (DISEÑO PREMIUM BRISA) ---
st.markdown("""
<style>
    /* Estilos para la barra lateral y botones */
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 10px rgba(0, 242, 254, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(0, 242, 254, 0.4);
        color: #11111d;
    }
    /* Estilo del botón de peligro */
    div[data-testid="stMarkdownContainer"] + div .stButton>button[key*="Borrar"] {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
    }
    /* Estilo de las cajas de métricas */
    .metric-box {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #00f2fe;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- PANEL DE CONTROL LATERAL AVANZADO ---
with st.sidebar:
    st.markdown("<h1 style='text-align: left; color: #00f2fe; font-size: 28px;'>📂 Panel de Brisa</h1>", unsafe_allow_html=True)
    
    # Sección 1: Gestión de Chats
    st.markdown("### 💬 Conversaciones")
    if st.button("➕ Crear Nuevo Chat", use_container_width=True):
        nuevo_id = f"Chat {len(st.session_state['lista_chats']) + 1}"
        st.session_state["lista_chats"][nuevo_id] = []
        st.session_state["chat_actual"] = nuevo_id
        st.rerun()
    
    st.write("")
    
    # Renderizar lista de chats disponibles
    for nombre_chat in list(st.session_state["lista_chats"].keys()):
        # Resaltar el chat activo de forma visual
        es_activo = "▶️ " if nombre_chat == st.session_state["chat_actual"] else ""
        if st.button(f"{es_activo}{nombre_chat}", key=f"btn_{nombre_chat}", use_container_width=True):
            st.session_state["chat_actual"] = nombre_chat
            st.rerun()
            
    st.write("---")
    
    # Sección 2: Selector de Cerebro (Modelos) - Idea exclusiva
    st.markdown("### 🧠 Cerebro de la IA")
    modelo_elegido = st.selectbox(
        "Cambia el motor de Brisa:",
        ["Llama 3.3 (Recomendado - Ultra Inteligente)", "Mixtral (Lógica y Código Profundo)"]
    )
    
    if modelo_elegido == "Llama 3.3 (Recomendado - Ultra Inteligente)":
        MODELO_GROQ = "llama-3.3-70b-versatile"
    else:
        MODELO_GROQ = "mixtral-8x7b-32768"
        
    st.write("---")
    
    # Sección 3: Ajustes de Personalidad Psicológica
    st.markdown("### 🎭 Personalidad")
    tono = st.selectbox(
        "Tono de Brisa:",
        ["Amigable y Empática", "Sincera y Directa", "Crítica y Sarcástica"]
    )
    
    # Configuración fina del System Prompt en base al nombre "Brisa"
    if tono == "Amigable y Empática":
        instruccion_sistema = "Tu nombre es Brisa. Eres una asistente de IA súper compañera, cálida, empática y optimista. Usa emojis, sé muy alentadora y habla con el dialecto español rioplatense (usa el 'vos' y modismos argentinos naturales)."
    elif tono == "Sincera y Directa":
        instruccion_sistema = "Tu nombre es Brisa. Eres una asistente de IA extremadamente sincera, directa y realista. No uses rodeos ni adornos, di las cosas tal cual son, con honestidad brutal pero constructiva y útil. Habla de 'vos'."
    else:
        instruccion_sistema = "Tu nombre es Brisa. Eres una asistente de IA con mentalidad crítica, un toque sarcástica, picante e ingeniosa. Cuestiona las ideas del usuario con humor ácido y perspicacia inteligente. Habla de 'vos'."

    st.write("---")
    
    # Sección 4: Estadísticas del Chat Actual - Idea exclusiva
    st.markdown("### 📊 Datos en Vivo")
    total_mensajes = len(st.session_state["lista_chats"][st.session_state["chat_actual"]])
    st.markdown(f"""
    <div class='metric-box'>
        <span style='color: #888;'>Mensajes en este chat:</span><br>
        <b style='color: #00f2fe; font-size: 18px;'>{total_mensajes}</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Sección 5: Zona de Peligro (Reset total)
    if st.button("🗑️ Borrar Todo y Reiniciar", type="primary", use_container_width=True, key="BorrarTodo"):
        st.session_state["lista_chats"] = {"Chat 1": []}
        st.session_state["chat_actual"] = "Chat 1"
        st.rerun()

# --- PANTALLA PRINCIPAL ---
st.markdown(f"<h1>🤖 Brisa IA Personal</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #8892b0;'>Conversación activa: <b>{st.session_state['chat_actual']}</b> | Personalidad: <b>{tono}</b></p>", unsafe_allow_html=True)

# Obtener historial del chat activo
historial_actual = st.session_state["lista_chats"][st.session_state["chat_actual"]]

# Mostrar mensajes históricos en pantalla
for mensaje in historial_actual:
    with st.chat_message(mensaje["role"]):
        st.write(mensaje["content"])

# Entrada de texto del usuario
if pregunta_usuario := st.chat_input("Escribe un mensaje para Brisa..."):
    # Guardar mensaje del usuario en memoria
    historial_actual.append({"role": "user", "content": pregunta_usuario})
    with st.chat_message("user"):
        st.write(pregunta_usuario)

    # Procesar respuesta con animación de carga profesional
    with st.chat_message("assistant"):
        with st.spinner("Brisa está procesando tu respuesta..."):
            # Construir el paquete completo: Personalidad del Sistema + Historial de Memoria completo
            mensajes_api = [{"role": "system", "content": instruccion_sistema}] + historial_actual
            
            completion = client.chat.completions.create(
                model=MODELO_GROQ,
                messages=mensajes_api
            )
            respuesta = completion.choices[0].message.content
        st.write(respuesta)
        
    # Guardar respuesta de Brisa en memoria
    historial_actual.append({"role": "assistant", "content": respuesta})
    st.session_state["lista_chats"][st.session_state["chat_actual"]] = historial_actual
