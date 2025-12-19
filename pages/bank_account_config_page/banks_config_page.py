import streamlit as st
from models.config_account_model import ConfigAccountModel
from .bank_account_controller import BankAccountController

controller = BankAccountController()


@st.dialog("Configuração de Conta")
def account_config_form(edit_id: int = None):
    account_model = ConfigAccountModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            account_model.id_account_config = existing.id_account_config
            account_model.account_name = existing.account_name
            account_model.balance = existing.balance
            account_model.investment_balance = existing.investment_balance
                    
    account_model.account_name = st.text_input(
        'Nome da Instituição Financeira', 
        value=account_model.account_name or "",
        key=f'nome_instituicao_{edit_id or "novo"}'
    )

    account_model.balance = st.number_input(
        'Saldo na conta',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=account_model.balance or 0.0,
        key=f'saldo_{edit_id or "novo"}'
    )

    account_model.investment_balance = st.number_input(
        'Valor Investido',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=account_model.investment_balance or 0.0,
        key=f'valor_investido_{edit_id or "novo"}'
    )
    
    if st.button("SALVAR", use_container_width=True, key=f'btn_save_account_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(account_model)
            st.session_state.refresh_table = True

        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(account_id: int, account_name: str):
    st.warning(f"Tem certeza que deseja excluir a conta **{account_name}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_{account_id}'):
            if controller.delete(account_id):
                st.session_state.refresh_table = True
                st.success("Conta deletada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar a conta")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_{account_id}'):
            st.rerun()


def account_config():
    st.subheader("Contas Bancárias")
    
    if st.button("➕ Nova Conta", use_container_width=True):
        account_config_form()
        
    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 2, 1.5, 1.5, 1.2])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Nome**")
        with header_cols[2]:
            st.write("**Saldo em Conta**")
        with header_cols[3]:
            st.write("**Valor Investido**")
        with header_cols[4]:
            st.write("**Ações**")
        
        st.divider()
        
        # Linhas de dados
        for row in data:
            row_cols = st.columns([1, 2, 1.5, 1.5, 1.2])
            
            with row_cols[0]:
                st.write(row.id_account_config)
            
            with row_cols[1]:
                st.write(row.account_name)
            
            with row_cols[2]:
                st.write(f"R$ {row.balance:.2f}")
            
            with row_cols[3]:
                st.write(f"R$ {row.investment_balance:.2f}")
            
            with row_cols[4]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_{row.id_account_config}', help="Editar"):
                        account_config_form(edit_id=row.id_account_config)
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_open_{row.id_account_config}', help="Deletar"):
                        delete_confirmation_dialog(row.id_account_config, row.account_name)
    else:
        st.info("Nenhuma conta cadastrada. Clique em '➕ Nova Conta' para começar.")


def show_bank_accounts_page():
    account_config()