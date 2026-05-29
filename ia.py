import streamlit as st
from groq import Groq

st.set_page_config(page_title="Brisa IA")

# --- CLAVE API ---
# Si esto falla, asegurate de que la clave sea exactamente la que te dio Groq
API_KEY = "gsk_Xre2owlZBcX8Zq3BdV8tWGdyb3FYJdjiyv9ty24jrSEuVJsTqpQ"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("Brisa IA en línea")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe algo..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state["messages"],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state["messages"].append({"role": "assistant", "content": response})
