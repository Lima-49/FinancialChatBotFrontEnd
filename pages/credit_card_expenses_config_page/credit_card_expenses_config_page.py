import streamlit as st
from datetime import datetime
from models.config_credit_card_invoice_model import ConfigCreditCardInvoiceModel
from .credit_card_expenses_controller import CreditCardExpensesController
from pages.credit_card_config_page.credit_card_controller import CreditCardController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = CreditCardExpensesController()
card_controller = CreditCardController()
account_controller = BankAccountController()


@st.dialog("Configuração de Fatura")
def invoice_config_form(edit_id: int = None):
    invoice_model = ConfigCreditCardInvoiceModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            invoice_model.invoice_id = existing.invoice_id
            invoice_model.card_id = existing.card_id
            invoice_model.account_id = existing.account_id
            invoice_model.invoice_month = existing.invoice_month
            invoice_model.invoice_year = existing.invoice_year
            invoice_model.invoice_amount = existing.invoice_amount
            invoice_model.is_paid = existing.is_paid
    
    # Cartão
    card_choices = [(row.id_card_config, row.card_name) for row in card_controller.list_all()]
    card_labels = [name for (_, name) in card_choices] or ["Nenhum cartão cadastrado"]
    
    # Find the current index
    if card_choices and invoice_model.card_id:
        card_idx = next((i for i, (card_id, _) in enumerate(card_choices) if card_id == invoice_model.card_id), 0)
    else:
        card_idx = 0
    
    card_idx = st.selectbox('Cartão de Crédito', options=list(range(len(card_labels))), format_func=lambda i: card_labels[i], index=card_idx, key=f'select_card_invoice_{edit_id or "novo"}') if card_choices else 0
    invoice_model.card_id = card_choices[card_idx][0] if card_choices else None

    # Banco
    account_choices = account_controller.get_choices()
    account_labels = [name for (_, name) in account_choices] or ["Nenhuma conta cadastrada"]
    
    # Find the current index
    if account_choices and invoice_model.account_id:
        account_idx = next((i for i, (account_id, _) in enumerate(account_choices) if account_id == invoice_model.account_id), 0)
    else:
        account_idx = 0
    
    account_idx = st.selectbox('Conta Associada', options=list(range(len(account_labels))), format_func=lambda i: account_labels[i], index=account_idx, key=f'select_account_invoice_{edit_id or "novo"}') if account_choices else 0
    invoice_model.account_id = account_choices[account_idx][0] if account_choices else None

    col1, col2 = st.columns(2)
    with col1:
        invoice_model.invoice_month = st.number_input(
            'Mês da Fatura',
            min_value=1,
            max_value=12,
            value=invoice_model.invoice_month or datetime.now().month,
            key=f'mes_fatura_{edit_id or "novo"}'
        )
    with col2:
        invoice_model.invoice_year = st.number_input(
            'Ano da Fatura',
            min_value=2020,
            max_value=2100,
            value=invoice_model.invoice_year or datetime.now().year,
            key=f'ano_fatura_{edit_id or "novo"}'
        )

    invoice_model.invoice_amount = st.number_input(
        'Valor da Fatura',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=float(invoice_model.invoice_amount) if invoice_model.invoice_amount else 0.0,
        key=f'valor_fatura_{edit_id or "novo"}'
    )

    invoice_model.is_paid = st.checkbox(
        'Fatura Paga',
        value=invoice_model.is_paid or False,
        key=f'fatura_paga_{edit_id or "novo"}'
    )

    if st.button("SALVAR", use_container_width=True, key=f'btn_save_invoice_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(invoice_model)
            st.session_state.refresh_table = True

        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(invoice_id: int, card_name: str, month: int, year: int):
    st.warning(f"Tem certeza que deseja excluir a fatura de **{card_name}** referente a **{month:02d}/{year}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_confirm_{invoice_id}'):
            if controller.delete(invoice_id):
                st.session_state.refresh_table = True
                st.success("Fatura deletada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar a fatura")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_delete_{invoice_id}'):
            st.rerun()


def invoice_config():
    st.subheader("Faturas de Cartões de Crédito")
    
    if st.button("➕ Nova Fatura", use_container_width=True):
        invoice_config_form()

    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 2, 1.2, 1, 1, 1, 1.5])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Cartão**")
        with header_cols[2]:
            st.write("**Período**")
        with header_cols[3]:
            st.write("**Valor**")
        with header_cols[4]:
            st.write("**Status**")
        with header_cols[5]:
            st.write("**Banco**")
        with header_cols[6]:
            st.write("**Ações**")
        
        st.divider()
        
        # Linhas de dados
        for row in data:
            row_cols = st.columns([1, 2, 1.2, 1, 1, 1, 1.5])
            
            with row_cols[0]:
                st.write(row.invoice_id)
            
            with row_cols[1]:
                st.write(row.card_id)
            
            with row_cols[2]:
                st.write(f"{row.invoice_month:02d}/{row.invoice_year}")
            
            with row_cols[3]:
                invoice_amount = row.invoice_amount or 0.0
                st.write(f"R$ {invoice_amount:.2f}")
            
            with row_cols[4]:
                status = "✅ Paga" if row.is_paid else "⏳ Pendente"
                st.write(status)
            
            with row_cols[5]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_invoice_{row.invoice_id}', help="Editar"):
                        invoice_config_form(edit_id=row.invoice_id)
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_invoice_{row.invoice_id}', help="Deletar"):
                        delete_confirmation_dialog(row.invoice_id, row.card_id, row.invoice_month, row.invoice_year)
    else:
        st.info("Nenhuma fatura cadastrada. Clique em '➕ Nova Fatura' para começar.")


def show_credit_card_expenses_page():
    invoice_config()
