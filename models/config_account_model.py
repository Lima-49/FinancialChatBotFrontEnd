class ConfigAccountModel:
    def __init__(self, account_name=None,
                  balance=None, id_account_config=None):
        self.id_account_config = id_account_config
        self.account_name = account_name
        self.balance = balance

    def from_dict(self, data):
        return ConfigAccountModel(
            id_account_config=data.get('id_account_config'),
            account_name = data.get('account_name'),
            balance = data.get('balance'),
        )
    
    def to_dict(self, data):
        return {
                "ID_ACCOUNT_CONFIG": data.id_account_config,
                "ACCOUNT_NAME": data.account_name,
                "BALANCE": data.balance,
            }
    