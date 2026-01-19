from __future__ import annotations

from typing import Dict, List
from database.db import get_connection
from models.config_regular_expenses_model import ConfigRegularExpensesModel
from config.config import get_table_name


class RegularExpensesService:
    def __init__(self) -> None:
        self.TABLE = get_table_name("SAIDAS_FREQUENTES")
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigRegularExpensesModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.regular_expense_id:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET NOME_SAIDA = %s, TIPO_SAIDA = %s, VALOR_SAIDA = %s, DIA_SAIDA = %s
                    WHERE ID_SAIDA_FREQUENTE = %s
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
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (NOME_SAIDA, TIPO_SAIDA, VALOR_SAIDA, DIA_SAIDA)
                VALUES (%s, %s, %s, %s) RETURNING ID_SAIDA_FREQUENTE
                """,
                (
                    model.regular_expense_name,
                    model.regular_expense_type,
                    model.regular_expense_amount or 0.0,
                    int(model.regular_expense_date or 1),
                ),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_saida_frequente'])

    def list_all(self) -> List[ConfigRegularExpensesModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} ORDER BY nome_saida"
            )
            return [ConfigRegularExpensesModel.from_dict(dict(row)) for row in cur.fetchall()]

    def get_by_id(self, regular_expense_id: int) -> ConfigRegularExpensesModel:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_SAIDA_FREQUENTE = %s",
                (regular_expense_id,),
            )
            row = cur.fetchone()
            return ConfigRegularExpensesModel.from_dict(dict(row)) if row else None

    def delete(self, regular_expense_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_SAIDA_FREQUENTE = %s",
                (regular_expense_id,),
            )
            conn.commit()
            return True
