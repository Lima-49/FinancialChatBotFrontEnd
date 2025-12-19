import streamlit as st
from models.config_purchase_limit_model import ConfigPurchaseLimitModel
from .purchase_limits_controller import PurchaseLimitsController
from pages.expenses_categories_config_page.expenses_categories_controller import ExpensesCategoriesController

controller = PurchaseLimitsController()
categories_controller = ExpensesCategoriesController()


@st.dialog("Configuração de Limite de Compra")
def limit_config_form(edit_id: int = None):
    limit_model = ConfigPurchaseLimitModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            limit_model.id_purchase_limit = existing.id_purchase_limit
            limit_model.id_purchase_category = existing.id_purchase_category
            limit_model.purchase_limit_amount = existing.purchase_limit_amount
    
    choices = categories_controller.get_choices()
    labels = [name for (_, name) in choices] or ["Nenhuma categoria cadastrada"]
    
    # Find the current index
    if choices and limit_model.id_purchase_category:
        idx = next((i for i, (cat_id, _) in enumerate(choices) if cat_id == limit_model.id_purchase_category), 0)
    else:
        idx = 0
    
    idx = st.selectbox('Categoria', options=list(range(len(labels))), format_func=lambda i: labels[i], index=idx, key=f'categoria_{edit_id or "novo"}') if choices else 0
    limit_model.id_purchase_category = choices[idx][0] if choices else None

    limit_model.purchase_limit_amount = st.number_input(
        'Limite da Categoria',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=limit_model.purchase_limit_amount or 0.0,
        key=f'limite_categoria_{edit_id or "novo"}'
    )

    if st.button("SALVAR", use_container_width=True, key=f'btn_save_limit_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(limit_model)
            st.session_state.refresh_table = True

        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(limit_id: int, category_name: str):
    st.warning(f"Tem certeza que deseja excluir o limite de **{category_name}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_confirm_{limit_id}'):
            if controller.delete(limit_id):
                st.session_state.refresh_table = True
                st.success("Limite deletado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar o limite")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_delete_{limit_id}'):
            st.rerun()


def limit_config():
    st.subheader("Limites de Compras")
    
    if st.button("➕ Novo Limite", use_container_width=True):
        limit_config_form()

    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 2, 1, 1.5])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Categoria**")
        with header_cols[2]:
            st.write("**Limite**")
        with header_cols[3]:
            st.write("**Ações**")
        
        st.divider()
        
        # Linhas de dados
        for row in data:
            row_cols = st.columns([1, 2, 1, 1.5])
            
            with row_cols[0]:
                st.write(row.id_purchase_limit)
            
            with row_cols[1]:
                st.write(row.category_name)
            
            with row_cols[2]:
                st.write(f"R$ {row.purchase_limit_amount:.2f}")
            
            with row_cols[3]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_limit_{row.id_purchase_limit}', help="Editar"):
                        limit_config_form(edit_id=row.id_purchase_limit)
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_limit_{row.id_purchase_limit}', help="Deletar"):
                        delete_confirmation_dialog(row.id_purchase_limit, row.category_name)
    else:
        st.info("Nenhum limite cadastrado. Clique em '➕ Novo Limite' para começar.")


def show_purchase_limits_page():
    limit_config()
