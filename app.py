import streamlit as st

st.set_page_config(page_title="Controle Financeiro", layout="centered")
st.title("Bem-vindo ao Controle Financeiro!")
st.write("Escolha uma página no menu lateral.")

st.session_state['account_config'] = None
st.session_state['card_config'] = None
st.session_state['entry_config'] = None
st.session_state['expenses_config'] = None