import streamlit as st
from models.config_purchase_limit_model import ConfigPurchaseLimitModel
from .purchase_limits_controller import PurchaseLimitsController
from pages.expenses_categories_config_page.expenses_categories_controller import ExpensesCategoriesController

controller = PurchaseLimitsController()
categories_controller = ExpensesCategoriesController()
limit_model = ConfigPurchaseLimitModel()


@st.dialog("Novo Limite de Compra")
def limit_config_form():
    
    choices = categories_controller.get_choices()
    labels = [name for (_, name) in choices] or ["Nenhuma categoria cadastrada"]
    idx = st.selectbox('Categoria', options=list(range(len(labels))), format_func=lambda i: labels[i]) if choices else 0
    limit_model.id_purchase_category = choices[idx][0] if choices else None

    limit_model.purchase_limit_amount = st.number_input(
        'Limite da Categoria',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='limite_categoria'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_limit'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(limit_model)
            limit_model.id_purchase_limit = new_id
            st.session_state['limit_config'] = limit_model

        st.rerun()


def limit_config():

    if st.button("Adicionar novo limite", key='btn_limit_config_form'):
        limit_config_form()
        
    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_limites')


def show_purchase_limits_page():
    limit_config()
