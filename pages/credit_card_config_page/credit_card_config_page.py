import streamlit as st
from models.config_card_model import ConfigCardModel, CardType
from .credit_card_controller import CreditCardController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = CreditCardController()
account_controller = BankAccountController()
card_model = ConfigCardModel()

@st.dialog("Nova Configuração")
def card_config_form():

    card_model.card_name = st.text_input(
        'Nome do Cartão',
        key='nome_cartao'
    )

    card_type_label = st.selectbox(
        'Tipo do Cartão',
        options=['Crédito', 'Débito'],
        key='select_card_type'
    )

    # vinculacao com conta
    choices = account_controller.get_choices()
    account_labels = [name for (_, name) in choices] or ["Nenhuma conta cadastrada"]
    selected_idx = st.selectbox('Conta Associada', options=list(range(len(account_labels))), format_func=lambda i: account_labels[i]) if choices else 0
    card_model.id_bank = choices[selected_idx][0] if choices else None

    card_model.date_due = st.number_input(
        'Dia do Vencimento',    
        min_value=1,
        max_value=31,
        value=1,
        key='date_due'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_card'):
        with st.spinner("Salvando configuração..."):

            card_model.card_type = CardType.CREDITO if card_type_label == 'Crédito' else CardType.DEBITO
            new_id = controller.save(card_model)
            card_model.id_card_config = new_id
            st.session_state['card_config'] = card_model

        st.rerun()

def card_config():
    
    if st.button("Adicionar novo cartão", key='btn_card_config_form'):
        card_config_form()

    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_cartoes')

def show_credit_card_page():
    card_config()