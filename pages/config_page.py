import streamlit as st
from models.config_account_model import ConfigAccountModel
from models.config_card_model import ConfigCardModel
from models.config_entry_model import ConfigEntryModel

class Config:
    def __init__(self) -> None:
        self.account_model = ConfigAccountModel()
        self.card_model = ConfigCardModel()
        self.entry_model = ConfigEntryModel()
        pass
    
    @st.dialog("Nova Configuração")
    def account_config_form(self):
                        
        self.account_model.account_name = st.text_input(
            'Nome da Instituição Financeira', 
            key='nome_instituicao_financeira'
        )

        self.account_model.balance = st.number_input(
            'Saldo na conta',
            min_value=0.0,
            step=0.01,
            format="%.2f",
            key='saldo'
        )
        
        if st.button("SALVAR", use_container_width=True, key='btn_save_account'):
            with st.spinner("Salvando configuração..."):

                #TODO: alterar o nome da função para salvar as configs
                self.controller.salvar_configuracao(self.account_model)
                st.session_state['account_config'] = self.account_model

            st.rerun()
          
    @st.dialog("Nova Configuração")
    def card_config_form(self):

        self.card_model.card_name = st.text_input(
            'Nome do Cartão',
            key='nome_cartao'
        )

        self.card_model.type = st.selectbox(
            'Tipo do Cartão',
            options=['Crédito', 'Débito'],
            key='select_card_type'
        )

        self.card_model.date_due = st.number_input(
            'Dia do Vencimento',    
            min_value=1,
            max_value=31,
            value=1,
            key='date_due'
        )

        if st.button("SALVAR", use_container_width=True, key='btn_save_card'):
            with st.spinner("Salvando configuração..."):

                #TODO: alterar o nome da função para salvar as configs
                self.controller.salvar_configuracao(self.card_model)
                st.session_state['card_config'] = self.card_model

            st.rerun()


    @st.dialog("Nova Configuração")
    def entry_config_form(self):
        
        self.entry_model.entry_name = st.text_input(
            'Nome da Entrada',
            key='nome_entrada'
        )

        self.entry_model.entry_type = st.selectbox(
            'Tipo da Entrada',
            options=['Salário', 'Presente', 'Beneficio', 'Outro'],
            key='select_entry_type'
        )

        self.entry_model.entry_account = st.selectbox(
            'Conta Associada',
            options=['Conta 1', 'Conta 2', 'Conta 3'],  # TODO: Fetch account names dynamically
            key='select_entry_account'
        )

        self.entry_model.amount = st.number_input(
            'Valor da Entrada',
            min_value=0.0,
            step=0.01,
            format="%.2f",
            key='amount'
        )

        self.entry_model.received_day = st.number_input(
            'Dia de Recebimento',
            min_value=1,
            max_value=31,
            value=1,
            key='received_day'
        )

        if st.button("SALVAR", use_container_width=True, key='btn_save_entry'):
            with st.spinner("Salvando configuração..."):

                #TODO: alterar o nome da função para salvar as configs
                self.controller.salvar_configuracao(self.entry_model)
                st.session_state['entry_config'] = self.entry_model

            st.rerun()

    def account_config(self):

        if st.button("Adicionar nova conta", key='btn_account_config_form'):
            self.account_config_form()
            
        if st.session_state['account_config'] is not None:
            #TODO: alterar para criar a visualizacao da tarefa
            df = self.controller.create_config_table_visualizatio(st.session_state['account_config'], self.config_tarefa_model.tipo_tarefa)
            if not df.empty:
                st.data_editor(df, num_rows="fixed", key='table_config_contas')
      
    def card_config(self):
        
        if st.button("Adicionar novo cartão", key='btn_card_config_form'):
            self.card_config_form()

        if st.session_state['card_config'] is not None:
            #TODO: alterar para criar a visualizacao da tarefa
            df = self.controller.create_config_table_visualizatio(st.session_state['card_config'], self.config_tarefa_model.tipo_tarefa)
            if not df.empty:
                st.data_editor(df, num_rows="fixed", key='table_config_cartoes')

    def entries_config(self):

        if st.button("Adicionar nova entrada", key='btn_entry_config_form'):
            self.entry_config_form()

        if st.session_state['entry_config'] is not None:
            #TODO: alterar para criar a visualizacao da tarefa
            df = self.controller.create_config_table_visualizatio(st.session_state['entry_config'], self.config_tarefa_model.tipo_tarefa)
            if not df.empty:
                st.data_editor(df, num_rows="fixed", key='table_config_entradas')


    def show(self):
        tabContas, tabCartoes, tabEntradas, tabBoletosRecorrentes, tabFaturas = st.tabs([
            'Contas', 
            'Cartões', 
            'Entradas',
            'Boletos Recorrentes',
            'Faturas'
        ])
        
        with tabContas:
            self.account_config()
            
        with tabCartoes:
            self.card_config()
            
        with tabEntradas:
            self.entries_config()
        
        with tabBoletosRecorrentes:
            st.write("Configurações de Boletos Recorrentes")
        
        with tabFaturas:
            st.write("Configurações de Faturas")
            
if __name__ == '__main__':
    config = Config()
    config.show()