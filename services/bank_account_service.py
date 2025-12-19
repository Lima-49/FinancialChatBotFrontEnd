from __future__ import annotations

from typing import Dict, List, Optional
from database.db import get_connection
from models.config_account_model import ConfigAccountModel


class BankAccountService:
    TABLE = "BANCOS"

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        # Tabela criada no Supabase via SQL script
        pass

    def save(self, model: ConfigAccountModel) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            if model.id_account_config:
                cur.execute(
                    f"""
                    UPDATE {self.TABLE}
                    SET NOME_BANCO=%s, VALOR_EM_CONTA=%s, VALOR_INVESTIDO=%s
                    WHERE ID_BANCO=%s
                    """,
                    (
                        model.account_name,
                        model.balance or 0,
                        model.investment_balance or 0,
                        model.id_account_config,
                    ),
                )
                conn.commit()
                return int(model.id_account_config)
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (NOME_BANCO, VALOR_EM_CONTA, VALOR_INVESTIDO)
                VALUES (%s, %s, %s) RETURNING ID_BANCO
                """,
                (model.account_name, model.balance or 0, model.investment_balance or 0),
            )
            result = cur.fetchone()
            conn.commit()
            return int(result['id_banco'])

    def list_all(self) -> List[ConfigAccountModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {self.TABLE} ORDER BY NOME_BANCO")
            rows = cur.fetchall()
            return [ConfigAccountModel.from_dict(dict(row)) for row in rows]

    def get_by_id(self, account_id: int) -> Optional[ConfigAccountModel]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ID_BANCO=%s",
                (account_id,),
            )
            row = cur.fetchone()
            return ConfigAccountModel.from_dict(dict(row)) if row else None

    def delete(self, account_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE ID_BANCO=%s",
                (account_id,),
            )
            conn.commit()
            return True
