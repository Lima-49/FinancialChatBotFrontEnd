import streamlit as st
from models.config_entry_model import ConfigEntryModel
from .entries_controller import EntriesController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = EntriesController()
account_controller = BankAccountController()
entry_model = ConfigEntryModel()

@st.dialog("Nova Configuração")
def entry_config_form():
    
    entry_model.entry_name = st.text_input(
        'Nome da Entrada',
        key='nome_entrada'
    )

    entry_model.entry_type = st.selectbox(
        'Tipo da Entrada',
        options=['Salário', 'Presente', 'Beneficio', 'Outro'],
        key='select_entry_type'
    )

    choices = account_controller.get_choices()
    labels = [name for (_, name) in choices] or ["Nenhuma conta cadastrada"]
    idx = st.selectbox('Conta Associada', options=list(range(len(labels))), format_func=lambda i: labels[i]) if choices else 0
    entry_model.account_id = choices[idx][0] if choices else None

    entry_model.amount = st.number_input(
        'Valor da Entrada',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='amount'
    )

    entry_model.received_day = st.number_input(
        'Dia de Recebimento',
        min_value=1,
        max_value=31,
        value=1,
        key='received_day'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_entry'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(entry_model)
            entry_model.entry_id = new_id
            st.session_state['entry_config'] = entry_model

        st.rerun()

def entries_config():

    if st.button("Adicionar nova entrada", key='btn_entry_config_form'):
        entry_config_form()

    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_entradas')

def show_entries_page():
    entries_config()