class ConfigCreditCardExpensesModel:
    def __init__(self, credit_card_expense_date=None, credit_card_shopping_name=None, credit_card_steps=None, credit_card_category_id=None, credit_card_value_amount=None, credit_card_observations=None, credit_card_expense_id=None, credit_card_id=None, account_id=None):
        self.credit_card_expense_id = credit_card_expense_id
        self.credit_card_id = credit_card_id
        self.account_id = account_id
        self.credit_card_expense_date = credit_card_expense_date
        self.credit_card_shopping_name = credit_card_shopping_name
        self.credit_card_steps = credit_card_steps
        self.credit_card_category_id = credit_card_category_id
        self.credit_card_value_amount = credit_card_value_amount
        self.credit_card_observations = credit_card_observations

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.
        Funciona com colunas em maiúsculo (SQLite) ou minúsculo (PostgreSQL)."""
        return cls(
            credit_card_expense_id=data.get('id_compra_cartao_credito') or data.get('ID_COMPRA_CARTAO_CREDITO'),
            credit_card_id=data.get('id_cartao') or data.get('ID_CARTAO'),
            account_id=data.get('id_banco') or data.get('ID_BANCO'),
            credit_card_expense_date=data.get('data_compra') or data.get('DATA_COMPRA'),
            credit_card_shopping_name=data.get('estabelecimento') or data.get('ESTABELECIMENTO'),
            credit_card_steps=data.get('parcelas') or data.get('PARCELAS'),
            credit_card_category_id=data.get('id_categoria') or data.get('ID_CATEGORIA'),
            credit_card_value_amount=data.get('valor_compra') or data.get('VALOR_COMPRA'),
            credit_card_observations=data.get('observacoes') or data.get('OBSERVACOES'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_compra_cartao_credito": self.credit_card_expense_id,
            "id_cartao": self.credit_card_id,
            "id_banco": self.account_id,
            "data_compra": self.credit_card_expense_date,
            "estabelecimento": self.credit_card_shopping_name,
            "parcelas": self.credit_card_steps,
            "id_categoria": self.credit_card_category_id,
            "valor_compra": self.credit_card_value_amount,
            "observacoes": self.credit_card_observations,
        }