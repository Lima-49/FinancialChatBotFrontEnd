from __future__ import annotations

from typing import List, Dict
from config.db import get_connection
from models.config_regular_expenses_model import ConfigRegularExpensesModel


class RegularExpensesController:
    TABLE = "SAIDAS_FREQUENTES"

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_SAIDA_FREQUENTE INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_BANCO INTEGER NOT NULL,
                    NOME_SAIDA TEXT NOT NULL,
                    TIPO_SAIDA TEXT NOT NULL,
                    VALOR_SAIDA REAL NOT NULL,
                    DIA_SAIDA INTEGER NOT NULL,
                    FOREIGN KEY (ID_BANCO) REFERENCES BANCOS(ID_BANCO)
                )
                """
            )

    def __init__(self) -> None:
        self._init_table()

    def save(self, model: ConfigRegularExpensesModel) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_BANCO, NOME_SAIDA, TIPO_SAIDA, VALOR_SAIDA, DIA_SAIDA)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    model.account_id,
                    model.regular_expense_name,
                    model.regular_expense_type,
                    model.regular_expense_amount or 0.0,
                    int(model.regular_expense_date or 1),
                ),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} ORDER BY NOME_SAIDA"
            )
            return [dict(r) for r in cur.fetchall()]
