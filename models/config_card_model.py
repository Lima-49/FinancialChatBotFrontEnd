from enum import Enum

class CardType(Enum):
    DEBITO = 0
    CREDITO = 1
    CREDITO_E_DEBITO = 2

class ConfigCardModel:
    def __init__(self, card_name=None, card_type=None, date_due=None, id_card_config=None, id_bank=None):
        self.id_card_config = id_card_config
        self.id_bank = id_bank
        self.card_name = card_name
        self.card_type = card_type
        self.date_due = date_due

    @classmethod
    def from_dict(cls, data):
        card_type_value = data.get('tipo_cartao')
        return cls(
            id_card_config=data.get('id_cartao'),
            id_bank=data.get('id_banco'),
            card_name=data.get('nome_cartao'),
            card_type=CardType(card_type_value) if card_type_value is not None else CardType.CREDITO,
            date_due=data.get('dia_vencimento'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_cartao": self.id_card_config,
            "id_banco": self.id_bank,
            "nome_cartao": self.card_name,
            "tipo_cartao": self.card_type.value if self.card_type else None,
            "dia_vencimento": self.date_due,
        }