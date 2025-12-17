import streamlit as st
from models.config_card_model import ConfigCardModel, CardType
from .credit_card_controller import CreditCardController
from pages.bank_account_config_page.bank_account_controller import BankAccountController

controller = CreditCardController()
account_controller = BankAccountController()


@st.dialog("Configuração de Cartão")
def card_config_form(edit_id: int = None):
    card_model = ConfigCardModel()
    
    # Se for edição, carrega dados existentes
    if edit_id:
        existing = controller.get_by_id(edit_id)
        if existing:
            card_model.id_card_config = existing["ID_CARTAO"]
            card_model.id_bank = existing["ID_BANCO"]
            card_model.card_name = existing["NOME_CARTAO"]
            card_model.card_type = CardType(existing["TIPO_CARTAO"])
            card_model.date_due = existing["DIA_VENCIMENTO"]

    card_model.card_name = st.text_input(
        'Nome do Cartão',
        value=card_model.card_name or "",
        key=f'nome_cartao_{edit_id or "novo"}'
    )

    card_type_label = st.selectbox(
        'Tipo do Cartão',
        options=['Crédito', 'Débito'],
        index=0 if card_model.card_type == CardType.CREDITO else 1 if card_model.card_type else 0,
        key=f'select_card_type_{edit_id or "novo"}'
    )

    choices = account_controller.get_choices()
    account_labels = [name for (_, name) in choices] or ["Nenhuma conta cadastrada"]
    selected_idx = st.selectbox('Conta Associada', options=list(range(len(account_labels))), format_func=lambda i: account_labels[i], key=f'conta_{edit_id or "novo"}') if choices else 0
    card_model.id_bank = choices[selected_idx][0] if choices else None

    card_model.date_due = st.number_input(
        'Dia do Vencimento',    
        min_value=1,
        max_value=31,
        value=card_model.date_due or 1,
        key=f'date_due_{edit_id or "novo"}'
    )

    if st.button("SALVAR", use_container_width=True, key=f'btn_save_card_{edit_id or "novo"}'):
        with st.spinner("Salvando configuração..."):
            card_model.card_type = CardType.CREDITO if card_type_label == 'Crédito' else CardType.DEBITO
            new_id = controller.save(card_model)
            st.session_state.refresh_table = True

        st.rerun()


@st.dialog("Confirmar Exclusão")
def delete_confirmation_dialog(card_id: int, card_name: str):
    st.warning(f"Tem certeza que deseja excluir o cartão **{card_name}**?")
    st.text("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Deletar", use_container_width=True, key=f'btn_delete_confirm_{card_id}'):
            if controller.delete(card_id):
                st.session_state.refresh_table = True
                st.success("Cartão deletado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar o cartão")
    
    with col2:
        if st.button("Cancelar", use_container_width=True, key=f'btn_cancel_delete_{card_id}'):
            st.rerun()


def card_config():
    st.subheader("Cartões de Crédito")
    
    if st.button("➕ Novo Cartão", use_container_width=True):
        card_config_form()

    data = controller.list_all()
    if data:
        # Header das colunas
        header_cols = st.columns([1, 2, 1.5, 1, 1, 1.2])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Nome**")
        with header_cols[2]:
            st.write("**Tipo**")
        with header_cols[3]:
            st.write("**Vencimento**")
        with header_cols[4]:
            st.write("**Banco**")
        with header_cols[5]:
            st.write("**Ações**")
        
        st.divider()
        
        # Linhas de dados
        for row in data:
            row_cols = st.columns([1, 2, 1.5, 1, 1, 1.2])
            
            with row_cols[0]:
                st.write(row["ID_CARTAO"])
            
            with row_cols[1]:
                st.write(row["NOME_CARTAO"])
            
            with row_cols[2]:
                tipo = "Crédito" if row["TIPO_CARTAO"] == 1 else "Débito"
                st.write(tipo)
            
            with row_cols[3]:
                st.write(f"Dia {row['DIA_VENCIMENTO']}")
            
            with row_cols[4]:
                st.write(row["NOME_BANCO"])
            
            with row_cols[5]:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("✏️", key=f'btn_edit_card_{row["ID_CARTAO"]}', help="Editar"):
                        card_config_form(edit_id=row["ID_CARTAO"])
                
                with btn_col2:
                    if st.button("🗑️", key=f'btn_delete_card_{row["ID_CARTAO"]}', help="Deletar"):
                        delete_confirmation_dialog(row["ID_CARTAO"], row["NOME_CARTAO"])
    else:
        st.info("Nenhum cartão cadastrado. Clique em '➕ Novo Cartão' para começar.")


def show_credit_card_page():
    card_config()