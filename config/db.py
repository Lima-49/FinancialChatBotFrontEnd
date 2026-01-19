from __future__ import annotations

import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL não encontrada. Configure o arquivo .env com suas credenciais do Supabase."
    )


def get_connection():
    """
    Retorna uma conexão com o banco PostgreSQL do Supabase.
    Usa RealDictCursor para retornar resultados como dicionários.
    """
    conn = psycopg2.connect(
        DATABASE_URL,
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    return conn
