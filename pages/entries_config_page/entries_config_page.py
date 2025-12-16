import streamlit as st
from models.config_entry_model import ConfigEntryModel

entry_model = ConfigEntryModel()

@st.dialog("Nova Configuração")
def entry_config_form():
    
    entry_model.entry_name = st.text_input(
        'Nome da Entrada',
        key='nome_entrada'
    )

    entry_model.entry_type = st.selectbox(
        'Tipo da Entrada',
        options=['Salário', 'Presente', 'Beneficio', 'Outro'],
        key='select_entry_type'
    )

    entry_model.entry_account = st.selectbox(
        'Conta Associada',
        options=['Conta 1', 'Conta 2', 'Conta 3'],  # TODO: Fetch account names dynamically
        key='select_entry_account'
    )

    entry_model.amount = st.number_input(
        'Valor da Entrada',
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key='amount'
    )

    entry_model.received_day = st.number_input(
        'Dia de Recebimento',
        min_value=1,
        max_value=31,
        value=1,
        key='received_day'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_entry'):
        with st.spinner("Salvando configuração..."):

            #TODO: alterar o nome da função para salvar as configs
            controller.salvar_configuracao(entry_model)
            st.session_state['entry_config'] = entry_model

        st.rerun()

def entries_config():

    if st.button("Adicionar nova entrada", key='btn_entry_config_form'):
        entry_config_form()

    if st.session_state['entry_config'] is not None:
        #TODO: alterar para criar a visualizacao da tarefa
        df = controller.create_config_table_visualizatio(st.session_state['entry_config'], entry_model.entry_type)
        if not df.empty:
            st.data_editor(df, num_rows="fixed", key='table_config_entradas')

def show_entries_page():
    entries_config()