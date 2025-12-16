from enum import Enum

class CardType(Enum):
    DEBITO = 0
    CREDITO = 1

class ConfigCardModel:
    def __init__(self, card_name=None, card_type=None, date_due=None, id_card_config=None, id_bank=None):
        self.id_card_config = id_card_config
        self.id_bank = id_bank
        self.card_name = card_name
        self.card_type = card_type
        self.date_due = date_due

    @staticmethod
    def from_dict(data):
        return ConfigCardModel(
            id_card_config=data.get('id_card_config'),
            id_bank=data.get('id_bank'),
            card_name=data.get('card_name'),
            card_type=CardType(data.get('card_type')) if data.get('card_type') is not None else 1,
            date_due=data.get('date_due'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_CARTAO": data.id_card_config,
            "ID_BANCO": data.id_bank,
            "NOME_CARTAO": data.card_name,
            "TIPO_CARTAO": data.card_type.value if data.card_type else None,
            "DIA_VENCIMENTO": data.date_due,
        }