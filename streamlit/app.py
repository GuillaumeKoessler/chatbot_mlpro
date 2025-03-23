import streamlit as st
import requests

st.title("Chatbot permettant de créer une poésie")

st.header("Permet de créer une poésie à partir d'un fichier .txt")

if "poeme" not in st.session_state:
    st.session_state.poeme = None

txt_file = st.file_uploader("Upload a file", type=["txt"])

if txt_file is not None:
    files = {"file": (txt_file.name, txt_file.read(), txt_file.type)}

    if st.button("Créer la poésie"):
        response = requests.post("http://localhost:8000/init_conv", files=files)

        if response.status_code == 200:
            st.session_state.poeme = response.json().get("poème")
        else:
            st.write("Error")

if st.session_state.poeme:
    st.write("Poème :")
    st.write(st.session_state.poeme)

    st.header("Chatbot sur le poème")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.chat_input("Entre ton message...")

    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        response_chat = requests.post(
            "http://localhost:8000/update", data={"request": user_input}, stream=True
        )

        if response_chat.status_code == 200:
            response_text = ""
            for chunk in response_chat.iter_lines():
                if chunk:
                    chunk_decoded = chunk.decode("utf-8")
                    response_text += chunk_decoded
            st.session_state.history.append({"role": "bot", "content": response_text})
        else:
            st.write("Error")

    for message in st.session_state.history:
        if message["role"] == "user":
            st.write("Vous : ", message["content"])
        else:
            st.write("Bot: ", message["content"])
