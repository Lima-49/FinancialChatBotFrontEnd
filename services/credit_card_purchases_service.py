from __future__ import annotations

from typing import List, Optional
from database.db import get_connection
from models.config_credit_card_expenses import ConfigCreditCardExpensesModel
from config.config import get_table_name


class CreditCardPurchasesService:
    def __init__(self) -> None:
        self.TABLE = get_table_name("COMPRAS_CARTOES_DE_CREDITO")
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigCreditCardExpensesModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.credit_card_expense_id:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_CARTAO=%s, ID_BANCO=%s, DATA_COMPRA=%s, ESTABELECIMENTO=%s,
                        PARCELAS=%s, ID_CATEGORIA=%s, VALOR_COMPRA=%s, OBSERVACOES=%s
                    WHERE ID_COMPRA_CARTAO_CREDITO=%s
                    """,
                    (
                        model.credit_card_id,
                        model.account_id,
                        model.credit_card_expense_date,
                        model.credit_card_shopping_name,
                        model.credit_card_steps,
                        model.credit_card_category_id,
                        model.credit_card_value_amount or 0.0,
                        model.credit_card_observations,
                        model.credit_card_expense_id,
                    ),
                )
                conn.commit()
                return int(model.credit_card_expense_id)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} 
                (ID_CARTAO, ID_BANCO, DATA_COMPRA, ESTABELECIMENTO, PARCELAS, 
                 ID_CATEGORIA, VALOR_COMPRA, OBSERVACOES)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING ID_COMPRA_CARTAO_CREDITO
                """,
                (
                    model.credit_card_id,
                    model.account_id,
                    model.credit_card_expense_date,
                    model.credit_card_shopping_name,
                    model.credit_card_steps,
                    model.credit_card_category_id,
                    model.credit_card_value_amount or 0.0,
                    model.credit_card_observations,
                ),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_compra_cartao_credito'])

    def list_all(self) -> List[ConfigCreditCardExpensesModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT c.*
                FROM {self.TABLE} c
                ORDER BY c.data_compra DESC
                """
            )
            return [ConfigCreditCardExpensesModel.from_dict(dict(row)) for row in cur.fetchall()]

    def get_by_id(self, purchase_id: int) -> Optional[ConfigCreditCardExpensesModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_COMPRA_CARTAO_CREDITO=%s",
                (purchase_id,),
            )
            row = cur.fetchone()
            return ConfigCreditCardExpensesModel.from_dict(dict(row)) if row else None

    def delete(self, purchase_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_COMPRA_CARTAO_CREDITO=%s",
                (purchase_id,),
            )
            conn.commit()
            return True
