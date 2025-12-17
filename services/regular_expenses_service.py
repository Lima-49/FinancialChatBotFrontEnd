from __future__ import annotations

from typing import Dict, List
from database.db import get_connection
from models.config_regular_expenses_model import ConfigRegularExpensesModel


class RegularExpensesService:
    TABLE = "SAIDAS_FREQUENTES"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_SAIDA_FREQUENTE INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOME_SAIDA TEXT NOT NULL,
                    TIPO_SAIDA TEXT NOT NULL,
                    VALOR_SAIDA REAL NOT NULL,
                    DIA_SAIDA INTEGER NOT NULL
                )
                """
            )

    def save(self, model: ConfigRegularExpensesModel) -> int:
        with get_connection() as conn:
            if model.regular_expense_id:
                conn.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET NOME_SAIDA = ?, TIPO_SAIDA = ?, VALOR_SAIDA = ?, DIA_SAIDA = ?
                    WHERE ID_SAIDA_FREQUENTE = ?
                    """,
                    (
                        model.regular_expense_name,
                        model.regular_expense_type,
                        model.regular_expense_amount or 0.0,
                        int(model.regular_expense_date or 1),
                        model.regular_expense_id,
                    ),
                )
                conn.commit()
                return model.regular_expense_id
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (NOME_SAIDA, TIPO_SAIDA, VALOR_SAIDA, DIA_SAIDA)
                VALUES (?, ?, ?, ?)
                """,
                (
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

    def get_by_id(self, regular_expense_id: int) -> Dict:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_SAIDA_FREQUENTE = ?",
                (regular_expense_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def delete(self, regular_expense_id: int) -> bool:
        with get_connection() as conn:
            conn.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_SAIDA_FREQUENTE = ?",
                (regular_expense_id,),
            )
            conn.commit()
            return True
