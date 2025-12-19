class ConfigAccountModel:
    def __init__(self, account_name=None,
                  balance=None, investment_balance=None, id_account_config=None):
        self.id_account_config = id_account_config
        self.account_name = account_name
        self.balance = balance
        self.investment_balance = investment_balance

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_account_config=data.get('id_banco'),
            account_name=data.get('nome_banco'),
            balance=data.get('valor_em_conta'),
            investment_balance=data.get('valor_investido')
        )
    
    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_banco": self.id_account_config,
            "nome_banco": self.account_name,
            "valor_em_conta": self.balance,
            "valor_investido": self.investment_balance
        }
    