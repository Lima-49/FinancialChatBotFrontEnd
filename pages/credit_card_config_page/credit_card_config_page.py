import streamlit as st
from models.config_card_model import ConfigCardModel

card_model = ConfigCardModel()

@st.dialog("Nova Configuração")
def card_config_form():

    card_model.card_name = st.text_input(
        'Nome do Cartão',
        key='nome_cartao'
    )

    card_model.type = st.selectbox(
        'Tipo do Cartão',
        options=['Crédito', 'Débito'],
        key='select_card_type'
    )

    card_model.date_due = st.number_input(
        'Dia do Vencimento',    
        min_value=1,
        max_value=31,
        value=1,
        key='date_due'
    )

    if st.button("SALVAR", use_container_width=True, key='btn_save_card'):
        with st.spinner("Salvando configuração..."):

            #TODO: alterar o nome da função para salvar as configs
            controller.salvar_configuracao(card_model)
            st.session_state['card_config'] = card_model

        st.rerun()

def card_config():
    
    if st.button("Adicionar novo cartão", key='btn_card_config_form'):
        card_config_form()

    if st.session_state['card_config'] is not None:
        #TODO: alterar para criar a visualizacao da tarefa
        df = controller.create_config_table_visualizatio(st.session_state['card_config'], config_tarefa_model.tipo_tarefa)
        if not df.empty:
            st.data_editor(df, num_rows="fixed", key='table_config_cartoes')

def show_credit_card_page():
    card_config()