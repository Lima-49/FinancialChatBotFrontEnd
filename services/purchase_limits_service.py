from __future__ import annotations

from typing import Dict, List, Optional
from database.db import get_connection
from models.config_purchase_limit_model import ConfigPurchaseLimitModel


class PurchaseLimitsService:
    TABLE = "LIMITES_COMPRAS"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigPurchaseLimitModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.id_purchase_limit:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_CATEGORIA=%s, LIMITE_CATEGORIA=%s
                    WHERE ID_LIMITE_COMPRA=%s
                    """,
                    (
                        model.id_purchase_category,
                        model.purchase_limit_amount or 0.0,
                        model.id_purchase_limit,
                    ),
                )
                conn.commit()
                return int(model.id_purchase_limit)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_CATEGORIA, LIMITE_CATEGORIA)
                VALUES (%s, %s) RETURNING ID_LIMITE_COMPRA
                """,
                (
                    model.id_purchase_category,
                    model.purchase_limit_amount or 0.0,
                ),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_limite_compra'])

    def list_all(self) -> List[ConfigPurchaseLimitModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT l.*
                FROM {self.TABLE} l
                LEFT JOIN CATEGORIAS_DE_COMPRAS c ON l.ID_CATEGORIA = c.ID_CATEGORIA
                ORDER BY c.nome_categoria
                """
            )
            return [ConfigPurchaseLimitModel.from_dict(dict(row)) for row in cur.fetchall()]

    def get_by_id(self, limit_id: int) -> Optional[ConfigPurchaseLimitModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_LIMITE_COMPRA=%s",
                (limit_id,),
            )
            row = cur.fetchone()
            return ConfigPurchaseLimitModel.from_dict(dict(row)) if row else None

    def delete(self, limit_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_LIMITE_COMPRA=%s",
                (limit_id,),
            )
            conn.commit()
            return True
