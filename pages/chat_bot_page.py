import streamlit as st
import json
import os
from controllers.chat_bot_controller import ChatBotController

class ChatBotPage:
    HISTORY_FILE = "chat_history.json"

    def __init__(self) -> None:
        st.set_page_config(page_title="Chatbot", layout="centered")
        self.chat_controller = ChatBotController()

        # initialize session state keys
        if "messages" not in st.session_state:
            st.session_state.messages = self.load_history()
        if "show_modal" not in st.session_state:
            st.session_state.show_modal = False


    @st.dialog("Anexe o PDF da sua fatura")
    def pdf_uploader(self):
        file_path = st.file_uploader(
            "Upload PDF", type=["pdf"]
        )
        password = st.text_input("Senha do arquivo, se tiver")

        if st.button("Submit"):
            if file_path is not None:
                st.session_state.pdf_uploader = f"{file_path}|||{password}"
                st.rerun()
                
            else:
                st.warning("Por favor, faça upload de um arquivo PDF.")

    def load_history(self):
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception:
                return []
        return []

    def save_history(self, messages):
        try:
            with open(self.HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(messages, file, ensure_ascii=False)
        except Exception:
            # ignore save errors for now
            pass

    def _show_clear_modal(self):
        st.warning("Tem certeza de que deseja limpar o histórico?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim, limpar", key="confirm_clear_yes"):
                st.session_state.messages = []
                self.save_history([])
                st.session_state.show_modal = False
                st.success("Histórico limpo com sucesso!")
                st.rerun()
        with col2:
            if st.button("Cancelar", key="confirm_clear_no"):
                st.session_state.show_modal = False
                st.rerun()

    def show(self):
        st.title("Chatbot")

        # Clear history button (opens simulated modal)
        if st.button("Limpar histórico", key="btn_clear_history"):
            st.session_state.show_modal = True

        if st.session_state.show_modal:
            self._show_clear_modal()

        col1, col2 = st.columns(2, vertical_alignment='bottom')

        with col1:
            # Chat input
            prompt = st.chat_input("Say something")

        with col2:
            if st.button("🗃️", key="btn_upload_pdf"):
                self.pdf_uploader()

        if st.session_state.pdf_uploader is not None:
            file_upload = st.session_state.pdf_uploader
            st.success("Arquivo PDF anexado com sucesso!")
        else:
            file_upload = None

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = self.chat_controller.get_chat_response(prompt, chat_history=st.session_state.messages, file_upload=file_upload)
            st.session_state.messages.append({"role": "bot", "content": response})
            self.save_history(st.session_state.messages)

        # Render chat history
        for message in st.session_state.messages:
            with st.chat_message(message.get("role", "user")):
                st.write(message.get("content", ""))
if __name__ == "__main__":
    page = ChatBotPage()
    page.show()