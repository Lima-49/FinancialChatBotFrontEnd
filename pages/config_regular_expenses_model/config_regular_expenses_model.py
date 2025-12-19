import streamlit as st
from models.config_regular_expenses_model import ConfigRegularExpensesModel
from .regular_expenses_controller import RegularExpensesController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = RegularExpensesController()
account_controller = BankAccountController()


@st.dialog("Configuração de Despesa Recorrente")
def expenses_config_form(edit_id: int = None):
    expenses_model = ConfigRegularExpensesModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            expenses_model.regular_expense_id = existing.regular_expense_id
            expenses_model.regular_expense_name = existing.regular_expense_name
            expenses_model.regular_expense_type = existing.regular_expense_type
            expenses_model.regular_expense_amount = existing.regular_expense_amount
            expenses_model.regular_expense_date = existing.regular_expense_date
    expenses_model.regular_expense_name = st.text_input(
        'Nome da Despesa', 
        value=expenses_model.regular_expense_name or "",
        key=f'nome_despesa_frequente_{edit_id or "novo"}'
    )

    expenses_model.regular_expense_type = st.text_input(
        'Tipo de Despesa', 
        value=expenses_model.regular_expense_type or "",
        key=f'tipo_despesa_frequente_{edit_id or "novo"}'
    )

    expenses_model.regular_expense_amount = st.number_input(
        'Valor da Despesa', 
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=expenses_model.regular_expense_amount or 0.0,
        key=f'valor_despesa_frequente_{edit_id or "novo"}'
    )

    expenses_model.regular_expense_date = st.number_input(
        'Dia de Vencimento da Despesa',
        min_value=1,
        max_value=31,
        value=expenses_model.regular_expense_date or 1,
        key=f'data_despesa_frequente_{edit_id or "novo"}'
    )  

    if st.button("SALVAR", use_container_width=True, key=f'btn_save_expense_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(expenses_model)
            st.session_state.refresh_table = True
        
        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(expense_id: int, expense_name: str):
    st.warning(f"Tem certeza que deseja excluir a despesa recorrente **{expense_name}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_confirm_{expense_id}'):
            if controller.delete(expense_id):
                st.session_state.refresh_table = True
                st.success("Despesa deletada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar a despesa")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_delete_{expense_id}'):
            st.rerun()


def expenses_config():
    st.subheader("Despesas Recorrentes")
    
    if st.button("➕ Nova Despesa Recorrente", use_container_width=True):
        expenses_config_form()

    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 2, 1.2, 1, 1, 1.5])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Nome**")
        with header_cols[2]:
            st.write("**Tipo**")
        with header_cols[3]:
            st.write("**Valor**")
        with header_cols[4]:
            st.write("**Dia**")
        with header_cols[5]:
            st.write("**Ações**")
        
        st.divider()
        
        # Linhas de dados
        for row in data:
            row_cols = st.columns([1, 2, 1.2, 1, 1, 1.5])
            
            with row_cols[0]:
                st.write(row.regular_expense_id)
            
            with row_cols[1]:
                st.write(row.regular_expense_name)
            
            with row_cols[2]:
                st.write(row.regular_expense_type)
            
            with row_cols[3]:
                st.write(f"R$ {row.regular_expense_amount:.2f}")
            
            with row_cols[4]:
                st.write(f"Dia {row.regular_expense_date}")
            
            with row_cols[5]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_expense_{row.regular_expense_id}', help="Editar"):
                        expenses_config_form(edit_id=row.regular_expense_id)
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_expense_{row.regular_expense_id}', help="Deletar"):
                        delete_confirmation_dialog(row.regular_expense_id, row.regular_expense_name)
    else:
        st.info("Nenhuma despesa recorrente cadastrada. Clique em '➕ Nova Despesa Recorrente' para começar.")


def show_expenses_page():
    expenses_config()