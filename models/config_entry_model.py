from enum import Enum

class CardType(Enum):
    DEBITO = 0
    CREDITO = 1

class ConfigEntryModel:
    def __init__(self, entry_name=None, entry_type=None, entry_account=None, amount=None, received_day=None, entry_id=None):
        self.entry_name = entry_name
        self.entry_type = entry_type
        self.entry_account = entry_account
        self.amount = amount
        self.received_day = received_day
        self.entry_id = entry_id

    @staticmethod
    def from_dict(data):
        return ConfigEntryModel(
            entry_name=data.get('entry_name'),
            entry_type=data.get('entry_type'),
            entry_account=data.get('entry_account'),
            amount=data.get('amount'),
            received_day=data.get('received_day'),
            entry_id=data.get('entry_id'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ENTRY_NAME": data.entry_name,
            "ENTRY_TYPE": data.entry_type,
            "ENTRY_ACCOUNT": data.entry_account,
            "AMOUNT": data.amount,
            "RECEIVED_DAY": data.received_day,
            "ENTRY_ID": data.entry_id
        }