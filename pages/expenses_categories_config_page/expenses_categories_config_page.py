import streamlit as st
from models.config_expenses_categories_model import ConfigExpensesCategoriesModel
from .expenses_categories_controller import ExpensesCategoriesController

controller = ExpensesCategoriesController()


@st.dialog("Configuração de Categoria")
def category_config_form(edit_id: int = None):
    category_model = ConfigExpensesCategoriesModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            category_model.category_id = existing["ID_CATEGORIA"]
            category_model.category_name = existing["NOME_CATEGORIA"]
    
    category_model.category_name = st.text_input(
        'Nome da Categoria',
        value=category_model.category_name or "",
        key=f'nome_categoria_{edit_id or "novo"}'
    )

    if st.button("SALVAR", use_container_width=True, key=f'btn_save_category_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(category_model)
            st.session_state.refresh_table = True

        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(category_id: int, category_name: str):
    st.warning(f"Tem certeza que deseja excluir a categoria **{category_name}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_confirm_{category_id}'):
            if controller.delete(category_id):
                st.session_state.refresh_table = True
                st.success("Categoria deletada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar a categoria")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_delete_{category_id}'):
            st.rerun()


def category_config():
    st.subheader("Categorias de Compras")
    
    if st.button("➕ Nova Categoria", use_container_width=True):
        category_config_form()

    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 3, 1.5])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Nome**")
        with header_cols[2]:
            st.write("**Ações**")
        
        st.divider()
        
        # Linhas de dados
        for row in data:
            row_cols = st.columns([1, 3, 1.5])
            
            with row_cols[0]:
                st.write(row["ID_CATEGORIA"])
            
            with row_cols[1]:
                st.write(row["NOME_CATEGORIA"])
            
            with row_cols[2]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_category_{row["ID_CATEGORIA"]}', help="Editar"):
                        category_config_form(edit_id=row["ID_CATEGORIA"])
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_category_{row["ID_CATEGORIA"]}', help="Deletar"):
                        delete_confirmation_dialog(row["ID_CATEGORIA"], row["NOME_CATEGORIA"])
    else:
        st.info("Nenhuma categoria cadastrada. Clique em '➕ Nova Categoria' para começar.")


def show_categories_page():
    category_config()
