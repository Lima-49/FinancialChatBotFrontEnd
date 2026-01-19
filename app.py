import streamlit as st
from config.config import is_test_mode

st.set_page_config(page_title="Controle Financeiro", layout="centered")

# Exibir indicador se em modo de teste
if is_test_mode():
    st.warning("Modo de Teste Ativado", icon="⚠️")

st.title("Bem-vindo ao Controle Financeiro!")
st.write("Escolha uma página no menu lateral.")

st.session_state['account_config'] = None
st.session_state['card_config'] = None
st.session_state['entry_config'] = None
st.session_state['expenses_config'] = None