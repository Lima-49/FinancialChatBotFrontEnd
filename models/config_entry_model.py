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

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.
        Funciona com colunas em maiúsculo (SQLite) ou minúsculo (PostgreSQL)."""
        return cls(
            entry_id=data.get('id_entrada') or data.get('ID_ENTRADA'),
            account_id=data.get('id_banco') or data.get('ID_BANCO'),
            entry_name=data.get('nome_entrada') or data.get('NOME_ENTRADA'),
            entry_type=data.get('tipo_entrada') or data.get('TIPO_ENTRADA'),
            amount=data.get('valor_entrada') or data.get('VALOR_ENTRADA'),
            received_day=data.get('dia_entrada') or data.get('DIA_ENTRADA'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_entrada": self.entry_id,
            "id_banco": self.account_id, 
            "nome_entrada": self.entry_name,
            "tipo_entrada": self.entry_type,
            "valor_entrada": self.amount,
            "dia_entrada": self.received_day,
        }