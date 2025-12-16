from __future__ import annotations

from typing import List, Dict, Optional
from config.db import get_connection
from models.config_expenses_categories_model import ConfigExpensesCategoriesModel


class ExpensesCategoriesController:
    TABLE = "CATEGORIAS_DE_COMPRAS"

    def _init_table(self) -> None:
        with get_connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    ID_CATEGORIA INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOME_CATEGORIA TEXT NOT NULL
                )
                """
            )

    def __init__(self) -> None:
        self._init_table()

    def save(self, model: ConfigExpensesCategoriesModel) -> int:
        with get_connection() as conn:
            if model.id_category:
                conn.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET NOME_CATEGORIA=?
                    WHERE ID_CATEGORIA=?
                    """,
                    (
                        model.category_name,
                        model.id_category,
                    ),
                )
                return int(model.id_category)
            cur = conn.execute(
                f"""
                INSERT INTO {self.TABLE} (NOME_CATEGORIA)
                VALUES (?)
                """,
                (model.category_name,),
            )
            return int(cur.lastrowid)

    def list_all(self) -> List[Dict]:
        with get_connection() as conn:
            cur = conn.execute(f"SELECT * FROM {self.TABLE} ORDER BY NOME_CATEGORIA")
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    def get_choices(self) -> List[tuple[int, str]]:
        data = self.list_all()
        return [(row["ID_CATEGORIA"], row["NOME_CATEGORIA"]) for row in data]

    def get_by_id(self, category_id: int) -> Optional[Dict]:
        with get_connection() as conn:
            cur = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_CATEGORIA=?", (category_id,)
            )
            row = cur.fetchone()
            return dict(row) if row else None
