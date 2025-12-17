from __future__ import annotations

from typing import List, Dict
from models.config_entry_model import ConfigEntryModel
from services.entries_service import EntriesService


class EntriesController:
    def __init__(self) -> None:
        self.service = EntriesService()

    def save(self, model: ConfigEntryModel) -> int:
        return self.service.save(model)

    def list_all(self) -> List[Dict]:
        return self.service.list_all()
    
    def get_by_id(self, entry_id: int) -> Dict:
        return self.service.get_by_id(entry_id)
    
    def delete(self, entry_id: int) -> bool:
        return self.service.delete(entry_id)
