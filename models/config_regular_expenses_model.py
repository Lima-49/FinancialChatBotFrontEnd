class ConfigRegularExpensesModel:
    def __init__(self, regular_expense_name=None, regular_expense_type=None, regular_expense_amount=None, regular_expense_date=None, regular_expense_id=None, account_id=None):
        self.regular_expense_id = regular_expense_id
        self.account_id = account_id
        self.regular_expense_name = regular_expense_name
        self.regular_expense_type = regular_expense_type
        self.regular_expense_amount = regular_expense_amount
        self.regular_expense_date = regular_expense_date

    @staticmethod
    def from_dict(data):
        return ConfigRegularExpensesModel(
            regular_expense_name=data.get('regular_expense_name'),
            regular_expense_type=data.get('regular_expense_type'),
            account_id=data.get('account_id'),
            regular_expense_amount=data.get('regular_expense_amount'),
            regular_expense_date=data.get('regular_expense_date'),
            regular_expense_id=data.get('regular_expense_id'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_SAIDA_FREQUENTE": data.regular_expense_id,
            "ID_BANCO": data.account_id, 
            "NOME_SAIDA": data.regular_expense_name,
            "TIPO_SAIDA": data.regular_expense_type,
            "VALOR_SAIDA": data.regular_expense_amount,
            "DATA_SAIDA": data.regular_expense_date,
        }