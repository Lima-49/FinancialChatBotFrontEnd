class ConfigExpensesCategoriesModel:
    def __init__(self, id_category=None, category_name=None):
        self.id_category = id_category
        self.category_name = category_name

    @staticmethod
    def from_dict(data):
        return ConfigExpensesCategoriesModel(
            id_category=data.get('id_category'),
            category_name=data.get('category_name'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_CATEGORIA": data.id_category,
            "NOME_CATEGORIA": data.category_name,
        }