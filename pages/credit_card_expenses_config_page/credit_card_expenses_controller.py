from __future__ import annotations

from typing import List, Optional
from models.config_credit_card_invoice_model import ConfigCreditCardInvoiceModel
from services.credit_card_expenses_service import CreditCardExpensesService


class CreditCardExpensesController:
    def __init__(self) -> None:
        self.service = CreditCardExpensesService()

    def save(self, model: ConfigCreditCardInvoiceModel) -> int:
        return self.service.save(model)

    def list_all(self) -> List[ConfigCreditCardInvoiceModel]:
        return self.service.list_all()

    def get_by_id(self, invoice_id: int) -> Optional[ConfigCreditCardInvoiceModel]:
        return self.service.get_by_id(invoice_id)

    def delete(self, invoice_id: int) -> bool:
        return self.service.delete(invoice_id)
