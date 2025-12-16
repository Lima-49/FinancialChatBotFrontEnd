from enum import Enum

class CardType(Enum):
    DEBITO = 0
    CREDITO = 1

class ConfigEntryModel:
    def __init__(self, entry_name=None, entry_type=None, entry_account=None, amount=None, received_day=None, entry_id=None, account_id=None):
        self.entry_id = entry_id
        self.account_id = account_id
        self.entry_name = entry_name
        self.entry_type = entry_type
        self.amount = amount
        self.received_day = received_day

    @staticmethod
    def from_dict(data):
        return ConfigEntryModel(
            entry_name=data.get('entry_name'),
            entry_type=data.get('entry_type'),
            account_id=data.get('account_id'),
            amount=data.get('amount'),
            received_day=data.get('received_day'),
            entry_id=data.get('entry_id'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_ENTRADA": data.entry_id,
            "ID_BANCO": data.account_id, 
            "NOME_ENTRADA": data.entry_name,
            "TIPO_ENTRADA": data.entry_type,
            "VALOR_ENTRADA": data.amount,
            "DATA_ENTRADA": data.received_day,
        }