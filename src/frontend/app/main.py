import streamlit as st
import requests

st.set_page_config(page_title="Chatbot", layout="wide")

st.title("Chatbot")

# -------------------------
# Sidebar - File upload
# -------------------------

with st.sidebar:
    st.header("KPI upload")

    uploaded_file = st.file_uploader(
        "Upload an Excel file",
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:
        if st.button("Send file", use_container_width=True):
            try:
                response = requests.post(
                    "http://kpi-api:8000/api",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    },
                )

                response.raise_for_status()

                result = response.json()

                st.success("File uploaded successfully!")

            except requests.RequestException as e:
                st.error(f"Upload failed: {e}")


# -------------------------
# Chat
# -------------------------

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

    response = response.json()["response"]

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)