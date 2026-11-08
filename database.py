
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

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS atendimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                produto_interesse TEXT NOT NULL,
                data TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pendente'
                    CHECK (status IN (
                        'Pendente',
                        'Em andamento',
                        'Concluído'
                    )),
                observacoes TEXT,
                FOREIGN KEY (cliente_id)
                    REFERENCES clientes(id)
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


def cadastrar_atendimento(
    cliente_id, produto_interesse, data, observacoes=None
):
    produto_interesse = produto_interesse.strip()

    if not produto_interesse:
        raise ValueError("O produto de interesse é obrigatório.")

    if not data:
        raise ValueError("A data é obrigatória.")

    with conectar() as conexao:
        cliente = conexao.execute(
            "SELECT id FROM clientes WHERE id = ?",
            (cliente_id,)
        ).fetchone()

        if cliente is None:
            raise ValueError("Cliente não encontrado.")

        cursor = conexao.execute(
            """
            INSERT INTO atendimentos
                (cliente_id, produto_interesse, data, observacoes)
            VALUES (?, ?, ?, ?)
            """,
            (cliente_id, produto_interesse, data, observacoes)
        )

        return cursor.lastrowid


def listar_atendimentos():
    with conectar() as conexao:
        registros = conexao.execute("""
            SELECT
                a.id,
                c.nome AS cliente,
                a.produto_interesse,
                a.data,
                a.status,
                a.observacoes
            FROM atendimentos a
            JOIN clientes c ON c.id = a.cliente_id
            ORDER BY a.id DESC
        """).fetchall()

        return [dict(atendimento) for atendimento in registros]
