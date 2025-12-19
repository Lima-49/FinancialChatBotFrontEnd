class ConfigRegularExpensesModel:
    def __init__(self, regular_expense_name=None, regular_expense_type=None, regular_expense_amount=None, regular_expense_date=None, regular_expense_id=None, account_id=None):
        self.regular_expense_id = regular_expense_id
        self.account_id = account_id
        self.regular_expense_name = regular_expense_name
        self.regular_expense_type = regular_expense_type
        self.regular_expense_amount = regular_expense_amount
        self.regular_expense_date = regular_expense_date

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.
        Funciona com colunas em maiúsculo (SQLite) ou minúsculo (PostgreSQL)."""
        return cls(
            regular_expense_id=data.get('id_saida_frequente') or data.get('ID_SAIDA_FREQUENTE'),
            account_id=data.get('id_banco') or data.get('ID_BANCO'),
            regular_expense_name=data.get('nome_saida') or data.get('NOME_SAIDA'),
            regular_expense_type=data.get('tipo_saida') or data.get('TIPO_SAIDA'),
            regular_expense_amount=data.get('valor_saida') or data.get('VALOR_SAIDA'),
            regular_expense_date=data.get('dia_saida') or data.get('DIA_SAIDA'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_saida_frequente": self.regular_expense_id,
            "id_banco": self.account_id, 
            "nome_saida": self.regular_expense_name,
            "tipo_saida": self.regular_expense_type,
            "valor_saida": self.regular_expense_amount,
            "dia_saida": self.regular_expense_date,
        }