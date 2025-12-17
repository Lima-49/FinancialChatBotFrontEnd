from __future__ import annotations

from typing import List, Dict, Optional
from models.config_purchase_limit_model import ConfigPurchaseLimitModel
from services.purchase_limits_service import PurchaseLimitsService


class PurchaseLimitsController:
    def __init__(self) -> None:
        self.service = PurchaseLimitsService()

    def save(self, model: ConfigPurchaseLimitModel) -> int:
        return self.service.save(model)

    def list_all(self) -> List[Dict]:
        return self.service.list_all()

    def get_by_id(self, limit_id: int) -> Optional[Dict]:
        return self.service.get_by_id(limit_id)

    def delete(self, limit_id: int) -> bool:
        return self.service.delete(limit_id)
