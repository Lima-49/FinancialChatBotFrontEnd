from __future__ import annotations

from typing import Dict, List
from database.db import get_connection
from models.config_entry_model import ConfigEntryModel


class EntriesService:
    TABLE = "ENTRADAS"

    def __init__(self) -> None:
        self._init_table()

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

    def save(self, model: ConfigEntryModel) -> int:
        with get_connection() as conn:
            if model.entry_id:
                conn.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_BANCO=?, NOME_ENTRADA=?, TIPO_ENTRADA=?, VALOR_ENTRADA=?, DIA_ENTRADA=?
                    WHERE ID_ENTRADA=?
                    """,
                    (
                        model.account_id,
                        model.entry_name,
                        model.entry_type,
                        model.amount or 0.0,
                        int(model.received_day or 1),
                        model.entry_id,
                    ),
                )
                return int(model.entry_id)
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

    def get_by_id(self, entry_id: int) -> Dict:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_ENTRADA=?",
                (entry_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def delete(self, entry_id: int) -> bool:
        with get_connection() as conn:
            conn.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_ENTRADA=?",
                (entry_id,),
            )
            conn.commit()
            return True
