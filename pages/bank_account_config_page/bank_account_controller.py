from __future__ import annotations

from typing import List, Dict, Optional
from config.db import get_connection
from models.config_account_model import ConfigAccountModel


class BankAccountController:
    TABLE = "BANCOS"

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_BANCO INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOME_BANCO TEXT NOT NULL,
                    VALOR_EM_CONTA REAL DEFAULT 0,
                    VALOR_INVESTIDO REAL DEFAULT 0
                )
                """
            )

    def __init__(self) -> None:
        self._init_table()

    def save(self, model: ConfigAccountModel) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (NOME_BANCO, VALOR_EM_CONTA, VALOR_INVESTIDO)
                VALUES (?, ?, ?)
                """,
                (model.account_name, model.balance or 0, model.investment_balance or 0),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(f"SELECT * FROM {self.TABLE} ORDER BY NOME_BANCO")
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    def get_choices(self) -> List[tuple[int, str]]:
        data = self.list_all()
        return [(row["ID_BANCO"], row["NOME_BANCO"]) for row in data]

    def get_by_id(self, account_id: int) -> Optional[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_BANCO=?", (account_id,)
            )
            row = cur.fetchone()
            return dict(row) if row else None
