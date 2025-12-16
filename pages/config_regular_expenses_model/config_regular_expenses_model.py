import streamlit as st
from models.config_regular_expenses_model import ConfigRegularExpensesModel

expenses_model = ConfigRegularExpensesModel()

@st.dialog("Nova Configuração")
def expenses_config_form():

    expenses_model.regular_expense_name = st.text_input(
        'Nome da Despesa', 
        key='nome_despesa_frequente'
    )

    expenses_model.regular_expense_type = st.text_input(
        'Tipo de Despesa', 
        key='tipo_despesa_frequente'
    )

    expenses_model.account_id = st.selectbox(
        'Conta Associada',
        options=["Conta 1", "Conta 2"],  # TODO: substituir por lista de contas reais
        key='conta_associada_despesa_frequente'
    )

    expenses_model.regular_expense_amount = st.number_input(
        'Valor da Despesa', 
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='valor_despesa_frequente'
    )

    expenses_model.regular_expense_date = st.number_input(
        'Dia de Vencimento da Despesa',
        min_value=1,
        max_value=31,
        value=1,
        key='data_despesa_frequente'
    )  

    if st.button("SALVAR", use_container_width=True, key='btn_save_expense'):
        with st.spinner("Salvando configuração..."):

            #TODO: alterar o nome da função para salvar as configs
            controller.salvar_configuracao(expenses_model)
            st.session_state['expenses_config'] = expenses_model
        
        st.rerun()

def expenses_config():

    if st.button("Adicionar nova despesa recorrente", key='btn_expense_config_form'):
        expenses_config_form()
        
    if st.session_state['expenses_config'] is not None:
        #TODO: alterar para criar a visualizacao da tarefa
        df = controller.create_config_table_visualizatio(st.session_state['account_config'], config_tarefa_model.tipo_tarefa)
        if not df.empty:
            st.data_editor(df, num_rows="fixed", key='table_config_contas')

def show_expenses_page():
    expenses_config()