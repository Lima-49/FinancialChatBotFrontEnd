class ConfigPurchaseLimitModel:
    def __init__(self, id_purchase_limit=None, id_purchase_category=None, purchase_limit_amount=None):
        self.id_purchase_limit = id_purchase_limit
        self.id_purchase_category = id_purchase_category
        self.purchase_limit_amount = purchase_limit_amount

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.
        Funciona com colunas em maiúsculo (SQLite) ou minúsculo (PostgreSQL)."""
        return cls(
            id_purchase_limit=data.get('id_limite_compra') or data.get('ID_LIMITE_COMPRA'),
            id_purchase_category=data.get('id_categoria') or data.get('ID_CATEGORIA'),
            purchase_limit_amount=data.get('limite_categoria') or data.get('LIMITE_CATEGORIA'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_limite_compra": self.id_purchase_limit,
            "id_categoria": self.id_purchase_category,
            "limite_categoria": self.purchase_limit_amount,
        }