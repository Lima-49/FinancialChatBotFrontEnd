import streamlit as st
from datetime import datetime
from models.config_credit_card_invoice_model import ConfigCreditCardInvoiceModel
from .credit_card_expenses_controller import CreditCardExpensesController
from pages.credit_card_config_page.credit_card_controller import CreditCardController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = CreditCardExpensesController()
card_controller = CreditCardController()
account_controller = BankAccountController()
invoice_model = ConfigCreditCardInvoiceModel()


@st.dialog("Nova Fatura de Cartão")
def invoice_config_form():
    
    # Cartão
    card_choices = [(row["ID_CARTAO"], row["NOME_CARTAO"]) for row in card_controller.list_all()]
    card_labels = [name for (_, name) in card_choices] or ["Nenhum cartão cadastrado"]
    card_idx = st.selectbox('Cartão de Crédito', options=list(range(len(card_labels))), format_func=lambda i: card_labels[i], key='select_card_invoice') if card_choices else 0
    invoice_model.card_id = card_choices[card_idx][0] if card_choices else None

    # Banco
    account_choices = account_controller.get_choices()
    account_labels = [name for (_, name) in account_choices] or ["Nenhuma conta cadastrada"]
    account_idx = st.selectbox('Conta Associada', options=list(range(len(account_labels))), format_func=lambda i: account_labels[i], key='select_account_invoice') if account_choices else 0
    invoice_model.account_id = account_choices[account_idx][0] if account_choices else None

    col1, col2 = st.columns(2)
    with col1:
        invoice_model.invoice_month = st.number_input(
            'Mês da Fatura',
            min_value=1,
            max_value=12,
            value=datetime.now().month,
            key='mes_fatura'
        )
    with col2:
        invoice_model.invoice_year = st.number_input(
            'Ano da Fatura',
            min_value=2020,
            max_value=2100,
            value=datetime.now().year,
            key='ano_fatura'
        )

    invoice_model.invoice_amount = st.number_input(
        'Valor da Fatura',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='valor_fatura'
    )

    invoice_model.is_paid = st.checkbox(
        'Fatura Paga',
        key='fatura_paga'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_invoice'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(invoice_model)
            invoice_model.invoice_id = new_id
            st.session_state['invoice_config'] = invoice_model

        st.rerun()


def invoice_config():

    if st.button("Adicionar nova fatura", key='btn_invoice_config_form'):
        invoice_config_form()
        
    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_faturas')


def show_credit_card_expenses_page():
    invoice_config()
