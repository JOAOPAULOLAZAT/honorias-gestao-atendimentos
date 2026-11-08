
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "honorias.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                canal TEXT NOT NULL
                    CHECK (canal IN ('WhatsApp', 'Instagram'))
            )
        """)


def cadastrar_cliente(nome, canal, telefone=None):
    nome = nome.strip()
    canal = canal.strip()
    telefone = telefone.strip() if telefone else None

    if not nome:
        raise ValueError("O nome do cliente é obrigatório.")

    if canal not in ("WhatsApp", "Instagram"):
        raise ValueError("Canal de contato inválido.")

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO clientes (nome, telefone, canal)
            VALUES (?, ?, ?)
            """,
            (nome, telefone, canal)
        )
        return cursor.lastrowid


def listar_clientes():
    with conectar() as conexao:
        registros = conexao.execute(
            "SELECT * FROM clientes ORDER BY nome"
        ).fetchall()
        return [dict(cliente) for cliente in registros]
