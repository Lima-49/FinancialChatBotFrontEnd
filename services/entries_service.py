from __future__ import annotations

from typing import Dict, List
from database.db import get_connection
from models.config_entry_model import ConfigEntryModel


class EntriesService:
    TABLE = "ENTRADAS"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigEntryModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.entry_id:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_BANCO=%s, NOME_ENTRADA=%s, TIPO_ENTRADA=%s, VALOR_ENTRADA=%s, DIA_ENTRADA=%s
                    WHERE ID_ENTRADA=%s
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
                conn.commit()
                return int(model.entry_id)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_BANCO, NOME_ENTRADA, TIPO_ENTRADA, VALOR_ENTRADA, DIA_ENTRADA)
                VALUES (%s, %s, %s, %s, %s) RETURNING ID_ENTRADA
                """,
                (
                    model.account_id,
                    model.entry_name,
                    model.entry_type,
                    model.amount or 0.0,
                    int(model.received_day or 1),
                ),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_entrada'])

    def list_all(self) -> List[ConfigEntryModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} ORDER BY nome_entrada"
            )
            return [ConfigEntryModel.from_dict(dict(row)) for row in cur.fetchall()]

    def get_by_id(self, entry_id: int) -> ConfigEntryModel:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_ENTRADA=%s",
                (entry_id,),
            )
            row = cur.fetchone()
            return ConfigEntryModel.from_dict(dict(row)) if row else None

    def delete(self, entry_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_ENTRADA=%s",
                (entry_id,),
            )
            conn.commit()
            return True
