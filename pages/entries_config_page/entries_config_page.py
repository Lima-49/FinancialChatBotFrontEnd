import streamlit as st
from models.config_entry_model import ConfigEntryModel
from .entries_controller import EntriesController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = EntriesController()
account_controller = BankAccountController()


@st.dialog("Configuração de Entrada")
def entry_config_form(edit_id: int = None):
    entry_model = ConfigEntryModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            entry_model.entry_id = existing.entry_id
            entry_model.account_id = existing.account_id
            entry_model.entry_name = existing.entry_name
            entry_model.entry_type = existing.entry_type
            entry_model.amount = existing.amount
            entry_model.received_day = existing.received_day
    
    entry_model.entry_name = st.text_input(
        'Nome da Entrada',
        value=entry_model.entry_name or "",
        key=f'nome_entrada_{edit_id or "novo"}'
    )

    entry_model.entry_type = st.selectbox(
        'Tipo da Entrada',
        options=['Salário', 'Presente', 'Beneficio', 'Outro'],
        index=['Salário', 'Presente', 'Beneficio', 'Outro'].index(entry_model.entry_type) if entry_model.entry_type in ['Salário', 'Presente', 'Beneficio', 'Outro'] else 0,
        key=f'select_entry_type_{edit_id or "novo"}'
    )

    choices = account_controller.get_choices()
    labels = [name for (_, name) in choices] or ["Nenhuma conta cadastrada"]
    idx = st.selectbox('Conta Associada', options=list(range(len(labels))), format_func=lambda i: labels[i], key=f'conta_{edit_id or "novo"}') if choices else 0
    entry_model.account_id = choices[idx][0] if choices else None

    entry_model.amount = st.number_input(
        'Valor da Entrada',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=float(entry_model.amount) if entry_model.amount else 0.0,
        key=f'amount_{edit_id or "novo"}'
    )

    entry_model.received_day = st.number_input(
        'Dia de Recebimento',
        min_value=1,
        max_value=31,
        value=entry_model.received_day or 1,
        key=f'received_day_{edit_id or "novo"}'
    )

    if st.button("SALVAR", use_container_width=True, key=f'btn_save_entry_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(entry_model)
            st.session_state.refresh_table = True

        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(entry_id: int, entry_name: str):
    st.warning(f"Tem certeza que deseja excluir a entrada **{entry_name}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_confirm_{entry_id}'):
            if controller.delete(entry_id):
                st.session_state.refresh_table = True
                st.success("Entrada deletada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar a entrada")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_delete_{entry_id}'):
            st.rerun()


def entries_config():
    st.subheader("Entradas")
    
    if st.button("➕ Nova Entrada", use_container_width=True):
        entry_config_form()

    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 2, 1.5, 1, 1, 1.2])
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
            row_cols = st.columns([1, 2, 1.5, 1, 1, 1.2])
            
            with row_cols[0]:
                st.write(row.entry_id)
            
            with row_cols[1]:
                st.write(row.entry_name)
            
            with row_cols[2]:
                st.write(row.entry_type)
            
            with row_cols[3]:
                st.write(f"R$ {row.amount:.2f}")
            
            with row_cols[4]:
                st.write(f"Dia {row.received_day}")
            
            with row_cols[5]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_entry_{row.entry_id}', help="Editar"):
                        entry_config_form(edit_id=row.entry_id)
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_entry_{row.entry_id}', help="Deletar"):
                        delete_confirmation_dialog(row.entry_id, row.entry_name)
    else:
        st.info("Nenhuma entrada cadastrada. Clique em '➕ Nova Entrada' para começar.")


def show_entries_page():
    entries_config()