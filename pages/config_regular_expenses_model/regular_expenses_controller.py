from __future__ import annotations

from typing import List, Dict
from models.config_regular_expenses_model import ConfigRegularExpensesModel
from services.regular_expenses_service import RegularExpensesService


class RegularExpensesController:
    def __init__(self) -> None:
        self.service = RegularExpensesService()

    def save(self, model: ConfigRegularExpensesModel) -> int:
        return self.service.save(model)

    def get_by_id(self, regular_expense_id: int) -> ConfigRegularExpensesModel:
        return self.service.get_by_id(regular_expense_id)

    def delete(self, regular_expense_id: int) -> bool:
        return self.service.delete(regular_expense_id)

    def list_all(self) -> List[ConfigRegularExpensesModel]:
        return self.service.list_all()
