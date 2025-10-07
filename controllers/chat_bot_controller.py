import requests

def route_request(user_input):
    # Regra simples: se contém "adicionar", "inserir", "novo gasto", envie para /insert
    if any(word in user_input.lower() for word in ["adicionar", "inserir", "novo gasto", "comprar", "gastei"]):
        return "/insert"
    else:
        return "/research"
    
def get_chat_response(prompt, chat_history=None):
    url = "http://localhost:8000/api/v1"  # URL do endpoint do chatbot
    
    if chat_history is None:
        chat_history = []
    
    
    payload = {"query": prompt,
               "chat_history": chat_history}
    
    headers = {"Content-Type": "application/json",
               "x-api-key": "secretKey"}
    
    try:
        route = route_request(prompt)
        response = requests.post(url+route, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("summary", "Desculpe, não consegui processar sua solicitação.")
    except requests.exceptions.RequestException as e:
        return f"Erro ao conectar com o chatbot: {e}"