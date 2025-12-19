from __future__ import annotations

from typing import Dict, List
from database.db import get_connection
from models.config_card_model import ConfigCardModel, CardType


class CreditCardService:
    TABLE = "CARTOES_DE_CREDITO"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigCardModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.id_card_config:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET ID_BANCO=%s, NOME_CARTAO=%s, TIPO_CARTAO=%s, DIA_VENCIMENTO=%s
                    WHERE ID_CARTAO=%s
                    """,
                    (
                        model.id_bank,
                        model.card_name,
                        (model.card_type.value if isinstance(model.card_type, CardType) else int(model.card_type)),
                        int(model.date_due or 1),
                        model.id_card_config,
                    ),
                )
                conn.commit()
                return int(model.id_card_config)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (ID_BANCO, NOME_CARTAO, TIPO_CARTAO, DIA_VENCIMENTO)
                VALUES (%s, %s, %s, %s) RETURNING ID_CARTAO
                """,
                (
                    model.id_bank,
                    model.card_name,
                    (model.card_type.value if isinstance(model.card_type, CardType) else int(model.card_type)),
                    int(model.date_due or 1),
                ),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_cartao'])

    def list_all(self) -> List[ConfigCardModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT c.*
                FROM {self.TABLE} c
                ORDER BY c.nome_cartao
                """
            )
            return [ConfigCardModel.from_dict(dict(row)) for row in cur.fetchall()]

    def get_by_id(self, card_id: int) -> ConfigCardModel:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_CARTAO=%s",
                (card_id,),
            )
            row = cur.fetchone()
            return ConfigCardModel.from_dict(dict(row)) if row else None

    def delete(self, card_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_CARTAO=%s",
                (card_id,),
            )
            conn.commit()
            return True
