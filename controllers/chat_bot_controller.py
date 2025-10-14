import re
import requests

class ChatBotController:
    def __init__(self):
        self.url = "http://localhost:8000/api/v1"

    def route_request(self, user_input, file_upload):
        # Regra simples: se contém "adicionar", "inserir", "novo gasto", envie para /insert
        if any(word in user_input.lower() for word in ["adicionar", "inserir", "novo gasto", "comprar", "gastei"]) and file_upload is None:
            return "/insert"
        elif file_upload is not None:
            return "/insertPdf"
        else:
            return "/research"

    def get_chat_response(self, prompt, chat_history=None, file_upload=None):
        
        if chat_history is None:
            chat_history = []
        

        if file_upload is None:
            payload = {"query": prompt,
                    "chat_history": chat_history}
        else:
            payload = {
                "query": prompt,
                "chat_history": chat_history,
                "file_path": file_upload.name,
                "file_content": file_upload.getvalue().decode("latin-1"),
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