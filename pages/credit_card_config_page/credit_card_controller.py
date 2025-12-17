from __future__ import annotations

from typing import List, Dict
from enum import Enum
from models.config_card_model import ConfigCardModel, CardType
from services.credit_card_service import CreditCardService


class CreditCardController:
    def __init__(self) -> None:
        self.service = CreditCardService()

    def save(self, model: ConfigCardModel) -> int:
        return self.service.save(model)

    def list_all(self) -> List[Dict]:
        return self.service.list_all()
    
    def get_by_id(self, card_id: int) -> Dict:
        return self.service.get_by_id(card_id)
    
    def delete(self, card_id: int) -> bool:
        return self.service.delete(card_id)
