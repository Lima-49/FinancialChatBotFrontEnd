from __future__ import annotations

from typing import List, Dict, Optional
from database.db import get_connection
from models.config_credit_card_invoice_model import ConfigCreditCardInvoiceModel


class CreditCardExpensesController:
    TABLE = "FATURAS_CARTOES_DE_CREDITO"

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_FATURA_CARTAO_CREDITO INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_CARTAO INTEGER NOT NULL,
                    ID_BANCO INTEGER NOT NULL,
                    MES_FATURA INTEGER NOT NULL,
                    ANO_FATURA INTEGER NOT NULL,
                    VALOR_FATURA REAL NOT NULL,
                    PAGA INTEGER DEFAULT 0,
                    FOREIGN KEY (ID_CARTAO) REFERENCES CARTOES_DE_CREDITO(ID_CARTAO),
                    FOREIGN KEY (ID_BANCO) REFERENCES BANCOS(ID_BANCO)
                )
                """
            )

    def __init__(self) -> None:
        self._init_table()

    def save(self, model: ConfigCreditCardInvoiceModel) -> int:
        with get_connection() as conn:
            if model.invoice_id:
                conn.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_CARTAO=?, ID_BANCO=?, MES_FATURA=?, ANO_FATURA=?, 
                        VALOR_FATURA=?, PAGA=?
                    WHERE ID_FATURA_CARTAO_CREDITO=?
                    """,
                    (
                        model.card_id,
                        model.account_id,
                        model.invoice_month,
                        model.invoice_year,
                        model.invoice_amount or 0.0,
                        1 if model.is_paid else 0,
                        model.invoice_id,
                    ),
                )
                return int(model.invoice_id)
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} 
                (ID_CARTAO, ID_BANCO, MES_FATURA, ANO_FATURA, VALOR_FATURA, PAGA)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    model.card_id,
                    model.account_id,
                    model.invoice_month,
                    model.invoice_year,
                    model.invoice_amount or 0.0,
                    1 if model.is_paid else 0,
                ),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"""
                SELECT f.*, c.NOME_CARTAO, b.NOME_BANCO
                FROM {self.TABLE} f
                LEFT JOIN CARTOES_DE_CREDITO c ON f.ID_CARTAO = c.ID_CARTAO
                LEFT JOIN BANCOS b ON f.ID_BANCO = b.ID_BANCO
                ORDER BY f.ANO_FATURA DESC, f.MES_FATURA DESC
                """
            )
            return [dict(r) for r in cur.fetchall()]

    def get_by_id(self, invoice_id: int) -> Optional[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_FATURA_CARTAO_CREDITO=?", (invoice_id,)
            )
            row = cur.fetchone()
            return dict(row) if row else None
