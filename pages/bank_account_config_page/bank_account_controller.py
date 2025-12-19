from __future__ import annotations

from typing import List, Dict, Optional
from models.config_account_model import ConfigAccountModel
from services.bank_account_service import BankAccountService


class BankAccountController:
    def __init__(self) -> None:
        self.service = BankAccountService()
        self.bank_account_model = ConfigAccountModel()

    def save(self, model: ConfigAccountModel) -> int:
        return self.service.save(model)

    def list_all(self) -> List[ConfigAccountModel]:
        return self.service.list_all()
        
    def get_choices(self) -> List[tuple[int, str]]:
        data = self.list_all()
        return [(row.id_account_config, row.account_name) for row in data]
    
    def get_by_id(self, account_id: int) -> Optional[ConfigAccountModel]:
        return self.service.get_by_id(account_id)

    def delete(self, account_id: int) -> bool:
        return self.service.delete(account_id)