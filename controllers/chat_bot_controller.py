import requests

class ChatBotController:
    def __init__(self):
        self.url = "http://localhost:8000/api/v1"

    def route_request(self, user_input):
        # Regra simples: se contém "adicionar", "inserir", "novo gasto", envie para /insert
        if any(word in user_input.lower() for word in ["adicionar", "inserir", "novo gasto", "comprar", "gastei"]):
            return "/insert"
        else:
            return "/research"
        
    def get_chat_response(self, prompt, chat_history=None, file_upload=None):
        if chat_history is None:
            chat_history = []
        
        payload = {"query": prompt,
                "chat_history": chat_history}
        
        headers = {"Content-Type": "application/json",
                "x-api-key": "secretKey"}
        
        try:
            route = self.route_request(prompt)
            response = requests.post(self.url+route, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get("summary", "Desculpe, não consegui processar sua solicitação.")
        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar com o chatbot: {e}"