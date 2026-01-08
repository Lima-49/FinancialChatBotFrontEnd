from __future__ import annotations

from typing import Dict, List, Optional
from database.db import get_connection
from models.config_credit_card_invoice_model import ConfigCreditCardInvoiceModel


class CreditCardExpensesService:
    TABLE = "FATURAS_CARTOES_DE_CREDITO"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigCreditCardInvoiceModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.invoice_id:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_CARTAO=%s, ID_BANCO=%s, MES_FATURA=%s, ANO_FATURA=%s, 
                        VALOR_FATURA=%s, PAGA=%s
                    WHERE ID_FATURA_CARTAO_CREDITO=%s
                    """,
                    (
                        model.card_id,
                        model.account_id,
                        model.invoice_month,
                        model.invoice_year,
                        model.invoice_amount or 0.0,
                        model.is_paid,
                        model.invoice_id,
                    ),
                )
                conn.commit()
                return int(model.invoice_id)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} 
                (ID_CARTAO, ID_BANCO, MES_FATURA, ANO_FATURA, VALOR_FATURA, PAGA)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID_FATURA_CARTAO_CREDITO
                """,
                (
                    model.card_id,
                    model.account_id,
                    model.invoice_month,
                    model.invoice_year,
                    model.invoice_amount or 0.0,
                    model.is_paid,
                ),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_fatura_cartao_credito'])

    def list_all(self) -> List[ConfigCreditCardInvoiceModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT f.*
                FROM {self.TABLE} f
                ORDER BY f.ano_fatura DESC, f.mes_fatura DESC
                """
            )
            return [ConfigCreditCardInvoiceModel.from_dict(dict(row)) for row in cur.fetchall()]
        
    def list_all_unpaid(self) -> List[ConfigCreditCardInvoiceModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT f.*
                FROM {self.TABLE} f
                WHERE f.paga = FALSE
                ORDER BY f.ano_fatura DESC, f.mes_fatura DESC
                """
            )
            return [ConfigCreditCardInvoiceModel.from_dict(dict(row)) for row in cur.fetchall()]

    def get_by_id(self, invoice_id: int) -> Optional[ConfigCreditCardInvoiceModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_FATURA_CARTAO_CREDITO=%s",
                (invoice_id,),
            )
            row = cur.fetchone()
            return ConfigCreditCardInvoiceModel.from_dict(dict(row)) if row else None

    def delete(self, invoice_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_FATURA_CARTAO_CREDITO=%s",
                (invoice_id,),
            )
            conn.commit()
            return True
