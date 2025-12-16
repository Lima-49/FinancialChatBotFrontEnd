import streamlit as st
from models.config_regular_expenses_model import ConfigRegularExpensesModel
from .regular_expenses_controller import RegularExpensesController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = RegularExpensesController()
account_controller = BankAccountController()
expenses_model = ConfigRegularExpensesModel()

@st.dialog("Nova Configuração")
def expenses_config_form():

    expenses_model.regular_expense_name = st.text_input(
        'Nome da Despesa', 
        key='nome_despesa_frequente'
    )

    expenses_model.regular_expense_type = st.text_input(
        'Tipo de Despesa', 
        key='tipo_despesa_frequente'
    )

    choices = account_controller.get_choices()
    labels = [name for (_, name) in choices] or ["Nenhuma conta cadastrada"]
    idx = st.selectbox('Conta Associada', options=list(range(len(labels))), format_func=lambda i: labels[i]) if choices else 0
    expenses_model.account_id = choices[idx][0] if choices else None

    expenses_model.regular_expense_amount = st.number_input(
        'Valor da Despesa', 
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='valor_despesa_frequente'
    )

    expenses_model.regular_expense_date = st.number_input(
        'Dia de Vencimento da Despesa',
        min_value=1,
        max_value=31,
        value=1,
        key='data_despesa_frequente'
    )  

    if st.button("SALVAR", use_container_width=True, key='btn_save_expense'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(expenses_model)
            expenses_model.regular_expense_id = new_id
            st.session_state['expenses_config'] = expenses_model
        
        st.rerun()

def expenses_config():

    if st.button("Adicionar nova despesa recorrente", key='btn_expense_config_form'):
        expenses_config_form()
        
    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_despesas_recorrentes')

def show_expenses_page():
    expenses_config()