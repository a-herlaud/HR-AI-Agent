import streamlit as st
import requests

st.set_page_config(page_title="Chatbot", layout="wide")

st.title("Chatbot")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Posez votre question..."):

    # Message utilisateur
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        "http://agent-system:8002/prompt",
        params={"prompt": prompt}
    )

    response.raise_for_status()
    response = response.json()
    response = response["response"]

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)