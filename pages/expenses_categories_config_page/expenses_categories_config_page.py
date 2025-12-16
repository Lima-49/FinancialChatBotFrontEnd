import streamlit as st
from models.config_expenses_categories_model import ConfigExpensesCategoriesModel
from .expenses_categories_controller import ExpensesCategoriesController

controller = ExpensesCategoriesController()
category_model = ConfigExpensesCategoriesModel()


@st.dialog("Nova Categoria")
def category_config_form():
    
    category_model.category_name = st.text_input(
        'Nome da Categoria',
        key='nome_categoria'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_category'):
        with st.spinner("Salvando configuração..."):
            new_id = controller.save(category_model)
            category_model.id_category = new_id
            st.session_state['category_config'] = category_model

        st.rerun()


def category_config():

    if st.button("Adicionar nova categoria", key='btn_category_config_form'):
        category_config_form()
        
    data = controller.list_all()
    if data:
        st.data_editor(data, num_rows="fixed", key='table_config_categorias')


def show_categories_page():
    category_config()
