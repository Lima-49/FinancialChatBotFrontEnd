from enum import Enum

class CardType(Enum):
    DEBITO = 0
    CREDITO = 1

class ConfigCardModel:
    def __init__(self, card_name=None, card_type=None, date_due=None, id_card_config=None):
        self.card_name = card_name
        self.card_type = card_type
        self.date_due = date_due
        self.id_card_config = id_card_config

    @staticmethod
    def from_dict(data):
        return ConfigCardModel(
            card_name=data.get('card_name'),
            card_type=CardType(data.get('card_type')) if data.get('card_type') is not None else None,
            date_due=data.get('date_due'),
            id_card_config=data.get('id_card_config'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "CARD_NAME": data.card_name,
            "CARD_TYPE": data.card_type.value if data.card_type else None,
            "DATE_DUE": data.date_due,
            "ID_CARD_CONFIG": data.id_card_config
        }