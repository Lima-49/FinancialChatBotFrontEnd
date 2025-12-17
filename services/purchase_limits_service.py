from __future__ import annotations

from typing import Dict, List, Optional
from database.db import get_connection
from models.config_purchase_limit_model import ConfigPurchaseLimitModel


class PurchaseLimitsService:
    TABLE = "LIMITES_COMPRAS"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_LIMITE_COMPRA INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_CATEGORIA INTEGER NOT NULL,
                    LIMITE_CATEGORIA REAL NOT NULL,
                    FOREIGN KEY (ID_CATEGORIA) REFERENCES CATEGORIAS_DE_COMPRAS(ID_CATEGORIA)
                )
                """
            )

    def save(self, model: ConfigPurchaseLimitModel) -> int:
        with get_connection() as conn:
            if model.id_purchase_limit:
                conn.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_CATEGORIA=?, LIMITE_CATEGORIA=?
                    WHERE ID_LIMITE_COMPRA=?
                    """,
                    (
                        model.id_purchase_category,
                        model.purchase_limit_amount or 0.0,
                        model.id_purchase_limit,
                    ),
                )
                return int(model.id_purchase_limit)
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_CATEGORIA, LIMITE_CATEGORIA)
                VALUES (?, ?)
                """,
                (
                    model.id_purchase_category,
                    model.purchase_limit_amount or 0.0,
                ),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"""
                SELECT l.*, c.NOME_CATEGORIA 
                FROM {self.TABLE} l
                LEFT JOIN CATEGORIAS_DE_COMPRAS c ON l.ID_CATEGORIA = c.ID_CATEGORIA
                ORDER BY c.NOME_CATEGORIA
                """
            )
            return [dict(r) for r in cur.fetchall()]

    def get_by_id(self, limit_id: int) -> Optional[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_LIMITE_COMPRA=?",
                (limit_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def delete(self, limit_id: int) -> bool:
        with get_connection() as conn:
            conn.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_LIMITE_COMPRA=?",
                (limit_id,),
            )
            conn.commit()
            return True
