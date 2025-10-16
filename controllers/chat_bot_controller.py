import re
import requests
import base64

class ChatBotController:
    def __init__(self):
        self.url = "http://localhost:8000/api/v1"

    def adjust_chat_history(self, chat_history):
        adjusted_history = []
        for message in chat_history:
            if message["role"] == "user":
                content = message["content"]
                content = content.text
                adjusted_history.append({"role": "user", "text": content})
            elif message["role"] == "assistant":
                adjusted_history.append({"role": "assistant", "text": message["content"]})
        return adjusted_history
    
    def route_request(self, user_input, file_upload):
        # Regra simples: se contém "adicionar", "inserir", "novo gasto", envie para /insert
        if any(word in user_input.text.lower() for word in ["adicionar", "inserir", "novo gasto", "comprar", "gastei"]) and file_upload is None:
            return "/insert"
        elif file_upload is not None:
            return "/insertPdf"
        else:
            return "/research"
        
    def _file_to_base64(self, uploaded_file):
        file_bytes = uploaded_file.read()
        file_b64 = base64.b64encode(file_bytes).decode("utf-8")
        return uploaded_file.name, file_b64

    def get_chat_response(self, prompt, chat_history=None, file_upload=None):
        
        if chat_history is None:
            chat_history = []
        else:
            chat_history = self.adjust_chat_history(chat_history)
        

        if file_upload is None:
            payload = {"query": prompt.text,
                    "chat_history": chat_history}
        else:
            payload = {
                "query": prompt,
                "chat_history": chat_history,
                "file_path": file_upload.name,
                "file_content": self._file_to_base64(file_upload),
            }

        headers = {"Content-Type": "application/json",
                "x-api-key": "secretKey"}
        
        try:
            route = self.route_request(prompt, file_upload)
            response = requests.post(self.url+route, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get("summary", "Desculpe, não consegui processar sua solicitação.")
        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar com o chatbot: {e}"