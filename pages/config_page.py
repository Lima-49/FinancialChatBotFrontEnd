import streamlit as st
from pages.bank_account_config_page.banks_config_page import show_bank_accounts_page
from pages.credit_card_config_page.credit_card_config_page import show_credit_card_page
from pages.entries_config_page.entries_config_page import show_entries_page
from pages.config_regular_expenses_model.config_regular_expenses_model import show_expenses_page

class Config:
    def __init__(self) -> None:
        pass
    

    def show(self):
        tabContas, tabCartoes, tabEntradas, tabBoletosRecorrentes, tabFaturas = st.tabs([
            'Contas', 
            'Cartões', 
            'Entradas',
            'Boletos Recorrentes',
            'Faturas'
        ])
        
        with tabContas:
            show_bank_accounts_page()
            
        with tabCartoes:
            show_credit_card_page()
            
        with tabEntradas:
            show_entries_page()
        
        with tabBoletosRecorrentes:
            show_expenses_page()
        
        with tabFaturas:
            st.write("Configurações de Faturas")
            
if __name__ == '__main__':
    config = Config()
    config.show()