import streamlit as st
from models.config_account_model import ConfigAccountModel
from .bank_account_controller import BankAccountController

controller = BankAccountController()
account_model = ConfigAccountModel()


@st.dialog("Nova Configuração")
def account_config_form():
                    
    account_model.account_name = st.text_input(
        'Nome da Instituição Financeira', 
        key='nome_instituicao_financeira'
    )

    account_model.balance = st.number_input(
        'Saldo na conta',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='saldo'
    )

    account_model.investment_balance = st.number_input(
        'Valor Investido',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='valor_investido'
    )
    
    if st.button("SALVAR", use_container_width=True, key='btn_save_account'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(account_model)
            account_model.id_account_config = new_id
            st.session_state['account_config'] = account_model

        st.rerun()


def account_config():

    if st.button("Adicionar nova conta", key='btn_account_config_form'):
        account_config_form()
        
    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_contas')

def show_bank_accounts_page():
    account_config()