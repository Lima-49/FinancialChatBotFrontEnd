import streamlit as st
import json
import os
from controllers.chat_bot_controller import get_chat_response

st.set_page_config(page_title="Chatbot", layout="centered")

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

def save_history(messages):
    with open(HISTORY_FILE, "w") as file:
        json.dump(messages, file)

st.title("Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = load_history()
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

if st.button("Limpar histórico"):
    st.session_state.show_modal = True

if st.session_state.show_modal:
    st.warning("Tem certeza de que deseja limpar o histórico?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sim, limpar"):
            st.session_state.messages = []
            save_history([])
            st.session_state.show_modal = False
            st.success("Histórico limpo com sucesso!")
    with col2:
        if st.button("Cancelar"):
            st.session_state.show_modal = False

prompt = st.chat_input("Say something")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_chat_response(prompt, chat_history=st.session_state.messages)
    st.session_state.messages.append({"role": "bot", "content": response})
    save_history(st.session_state.messages)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])