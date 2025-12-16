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

    @staticmethod
    def from_dict(data):
        return ConfigCreditCardExpensesModel(
            credit_card_expense_id=data.get('credit_card_expense_id'),
            credit_card_id=data.get('credit_card_id'),
            account_id=data.get('account_id'),
            credit_card_expense_date=data.get('credit_card_expense_date'),
            credit_card_shopping_name=data.get('credit_card_shopping_name'),
            credit_card_steps=data.get('credit_card_steps'),
            credit_card_category_id=data.get('credit_card_category_id'),
            credit_card_value_amount=data.get('credit_card_value_amount'),
            credit_card_observations=data.get('credit_card_observations'),
            
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_COMPRA_CARTAO_CREDITO": data.credit_card_expense_id,
            "ID_CARTAO": data.credit_card_id,
            "ID_BANCO": data.account_id,
            "DATA_COMPRA": data.credit_card_expense_date,
            "ESTABELECIMENTO": data.credit_card_shopping_name,
            "PARCELAS": data.credit_card_steps,
            "ID_CATEGORIA": data.credit_card_category_id,
            "VALOR_COMPRA": data.credit_card_value_amount,
            "OBSERVACOES": data.credit_card_observations,

        }