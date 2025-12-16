class ConfigAccountModel:
    def __init__(self, account_name=None,
                  balance=None, investment_balance=None, id_account_config=None):
        self.id_account_config = id_account_config
        self.account_name = account_name
        self.balance = balance
        self.investment_balance = investment_balance

    def from_dict(self, data):
        return ConfigAccountModel(
            id_account_config=data.get('id_account_config'),
            account_name = data.get('account_name'),
            balance = data.get('balance'),
            investment_balance = data.get('investment_balance')
        )
    
    def to_dict(self, data):
        return {
                "ID_BANCO": data.id_account_config,
                "NOME_BANCO": data.account_name,
                "VALOR_EM_CONTA": data.balance,
                "VALOR_INVESTIDO": data.investment_balance
            }
    