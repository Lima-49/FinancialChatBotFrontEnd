from __future__ import annotations

from typing import Dict, List, Optional
from database.db import get_connection
from models.config_expenses_categories_model import ConfigExpensesCategoriesModel


class ExpensesCategoriesService:
    TABLE = "CATEGORIAS_DE_COMPRAS"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigExpensesCategoriesModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.id_category:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET NOME_CATEGORIA=%s
                    WHERE ID_CATEGORIA=%s
                    """,
                    (
                        model.category_name,
                        model.id_category,
                    ),
                )
                conn.commit()
                return int(model.id_category)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (NOME_CATEGORIA)
                VALUES (%s) RETURNING ID_CATEGORIA
                """,
                (model.category_name,),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_categoria'])

    def list_all(self) -> List[ConfigExpensesCategoriesModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {self.TABLE} ORDER BY nome_categoria")
            rows = cur.fetchall()
            return [ConfigExpensesCategoriesModel.from_dict(dict(row)) for row in rows]

    def get_by_id(self, category_id: int) -> Optional[ConfigExpensesCategoriesModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_CATEGORIA=%s",
                (category_id,),
            )
            row = cur.fetchone()
            return ConfigExpensesCategoriesModel.from_dict(dict(row)) if row else None

    def delete(self, category_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_CATEGORIA=%s",
                (category_id,),
            )
            conn.commit()
            return True
