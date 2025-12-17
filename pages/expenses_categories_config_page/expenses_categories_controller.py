from __future__ import annotations

from typing import List, Dict, Optional
from models.config_expenses_categories_model import ConfigExpensesCategoriesModel
from services.expenses_categories_service import ExpensesCategoriesService


class ExpensesCategoriesController:
    def __init__(self) -> None:
        self.service = ExpensesCategoriesService()

    def save(self, model: ConfigExpensesCategoriesModel) -> int:
        return self.service.save(model)

    def list_all(self) -> List[Dict]:
        return self.service.list_all()

    def get_choices(self) -> List[tuple[int, str]]:
        data = self.list_all()
        return [(row["ID_CATEGORIA"], row["NOME_CATEGORIA"]) for row in data]

    def get_by_id(self, category_id: int) -> Optional[Dict]:
        return self.service.get_by_id(category_id)

    def delete(self, category_id: int) -> bool:
        return self.service.delete(category_id)
