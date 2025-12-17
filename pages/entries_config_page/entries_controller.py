from __future__ import annotations

from typing import List, Dict
from database.db import get_connection
from models.config_entry_model import ConfigEntryModel


class EntriesController:
    TABLE = "ENTRADAS"

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_ENTRADA INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_BANCO INTEGER NOT NULL,
                    NOME_ENTRADA TEXT NOT NULL,
                    TIPO_ENTRADA TEXT NOT NULL,
                    VALOR_ENTRADA REAL NOT NULL,
                    DIA_ENTRADA INTEGER NOT NULL,
                    FOREIGN KEY (ID_BANCO) REFERENCES BANCOS(ID_BANCO)
                )
                """
            )

    def __init__(self) -> None:
        self._init_table()

    def save(self, model: ConfigEntryModel) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_BANCO, NOME_ENTRADA, TIPO_ENTRADA, VALOR_ENTRADA, DIA_ENTRADA)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    model.account_id,
                    model.entry_name,
                    model.entry_type,
                    model.amount or 0.0,
                    int(model.received_day or 1),
                ),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} ORDER BY NOME_ENTRADA"
            )
            return [dict(r) for r in cur.fetchall()]
