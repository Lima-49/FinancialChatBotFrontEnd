class ConfigExpensesCategoriesModel:
    def __init__(self, id_category=None, category_name=None):
        self.id_category = id_category
        self.category_name = category_name

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.
        Funciona com colunas em maiúsculo (SQLite) ou minúsculo (PostgreSQL)."""
        return cls(
            id_category=data.get('id_categoria') or data.get('ID_CATEGORIA'),
            category_name=data.get('nome_categoria') or data.get('NOME_CATEGORIA'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_categoria": self.id_category,
            "nome_categoria": self.category_name,
        }