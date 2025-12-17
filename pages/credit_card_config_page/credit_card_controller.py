from __future__ import annotations

from typing import List, Dict
from enum import Enum
from database.db import get_connection
from models.config_card_model import ConfigCardModel, CardType


class CreditCardController:
    TABLE = "CARTOES_DE_CREDITO"

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_CARTAO INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_BANCO INTEGER NOT NULL,
                    NOME_CARTAO TEXT NOT NULL,
                    TIPO_CARTAO INTEGER NOT NULL,
                    DIA_VENCIMENTO INTEGER NOT NULL,
                    FOREIGN KEY (ID_BANCO) REFERENCES BANCOS(ID_BANCO)
                )
                """
            )

    def __init__(self) -> None:
        self._init_table()

    def save(self, model: ConfigCardModel) -> int:
        with get_connection() as conn:
            if model.id_card_config:
                conn.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_BANCO=?, NOME_CARTAO=?, TIPO_CARTAO=?, DIA_VENCIMENTO=?
                    WHERE ID_CARTAO=?
                    """,
                    (
                        model.id_bank,
                        model.card_name,
                        (model.card_type.value if isinstance(model.card_type, CardType) else int(model.card_type)),
                        int(model.date_due or 1),
                        model.id_card_config,
                    ),
                )
                return int(model.id_card_config)
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_BANCO, NOME_CARTAO, TIPO_CARTAO, DIA_VENCIMENTO)
                VALUES (?, ?, ?, ?)
                """,
                (
                    model.id_bank,
                    model.card_name,
                    (model.card_type.value if isinstance(model.card_type, CardType) else int(model.card_type)),
                    int(model.date_due or 1),
                ),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"""
                SELECT c.*, b.NOME_BANCO
                FROM {self.TABLE} c
                LEFT JOIN BANCOS b ON c.ID_BANCO = b.ID_BANCO
                ORDER BY c.NOME_CARTAO
                """
            )
            return [dict(r) for r in cur.fetchall()]
    
    def get_by_id(self, card_id: int) -> Dict:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_CARTAO=?", (card_id,)
            )
            row = cur.fetchone()
            return dict(row) if row else None
    
    def delete(self, card_id: int) -> bool:
        try:
            with get_connection() as conn:
                conn.execute(
                    f"DELETE FROM {self.TABLE} WHERE ID_CARTAO=?",
                    (card_id,)
                )
            return True
        except Exception:
            return False
