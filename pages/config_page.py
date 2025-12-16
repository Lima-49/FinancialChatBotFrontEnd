import streamlit as st
from pages.bank_account_config_page.banks_config_page import show_bank_accounts_page
from pages.credit_card_config_page.credit_card_config_page import show_credit_card_page
from pages.entries_config_page.entries_config_page import show_entries_page
from pages.config_regular_expenses_model.config_regular_expenses_model import show_expenses_page
from pages.expenses_categories_config_page.expenses_categories_config_page import show_categories_page
from pages.purchase_limits_config_page.purchase_limits_config_page import show_purchase_limits_page
from pages.credit_card_expenses_config_page.credit_card_expenses_config_page import show_credit_card_expenses_page

class Config:
    def __init__(self) -> None:
        pass
    

    def show(self):
        tabContas, tabCartoes, tabEntradas, tabBoletosRecorrentes, tabFaturas, tabCategorias, tabLimites = st.tabs([
            'Contas', 
            'Cartões', 
            'Entradas',
            'Boletos Recorrentes',
            'Faturas',
            'Categorias',
            'Limites'
        ])
        
        with tabContas:
            show_bank_accounts_page()
            
        with tabCartoes:
            show_credit_card_page()
            
        with tabEntradas:
            show_entries_page()
        
        with tabBoletosRecorrentes:
            st.write("Configurações de Boletos Recorrentes")
            show_expenses_page()
        
        with tabFaturas:
            show_credit_card_expenses_page()
        
        with tabCategorias:
            show_categories_page()
        
        with tabLimites:
            show_purchase_limits_page()
            
if __name__ == '__main__':
    config = Config()
    config.show()