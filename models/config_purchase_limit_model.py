class ConfigPurchaseLimitModel:
    def __init__(self, id_purchase_limit=None, id_purchase_category=None, purchase_limit_amount=None):
        self.id_purchase_limit = id_purchase_limit
        self.id_purchase_category = id_purchase_category
        self.purchase_limit_amount = purchase_limit_amount

    @staticmethod
    def from_dict(data):
        return ConfigPurchaseLimitModel(
            id_purchase_limit=data.get('id_purchase_limit'),
            id_purchase_category=data.get('id_purchase_category'),
            purchase_limit_amount=data.get('purchase_limit_amount'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_LIMITE_COMPRA": data.id_purchase_limit,
            "ID_CATEGORIA": data.id_purchase_category,
            "LIMITE_CATEGORIA": data.purchase_limit_amount,
        }