
import pytest
import database


@pytest.fixture
def banco_temporario(tmp_path, monkeypatch):
    caminho = tmp_path / "teste.db"
    monkeypatch.setattr(database, "DB_PATH", caminho)
    database.criar_tabelas()
    return caminho


def test_cadastrar_cliente(banco_temporario):
    cliente_id = database.cadastrar_cliente(
        "Cliente Exemplo", "WhatsApp"
    )

    clientes = database.listar_clientes()

    assert cliente_id > 0
    assert len(clientes) == 1
    assert clientes[0]["nome"] == "Cliente Exemplo"
    assert clientes[0]["canal"] == "WhatsApp"


def test_nome_obrigatorio(banco_temporario):
    with pytest.raises(ValueError):
        database.cadastrar_cliente("   ", "WhatsApp")


def test_canal_invalido(banco_temporario):
    with pytest.raises(ValueError):
        database.cadastrar_cliente("Cliente Exemplo", "Email")


def test_tipo_nome_invalido(banco_temporario):
    with pytest.raises(ValueError):
        database.cadastrar_cliente(None, "WhatsApp")


def test_registrar_atendimento(banco_temporario):
    cliente_id = database.cadastrar_cliente(
        "Cliente Exemplo", "Instagram"
    )

    atendimento_id = database.cadastrar_atendimento(
        cliente_id,
        "Pulseira Coração",
        "2026-11-07"
    )

    atendimentos = database.listar_atendimentos()

    assert atendimento_id > 0
    assert len(atendimentos) == 1
    assert atendimentos[0]["cliente"] == "Cliente Exemplo"
    assert atendimentos[0]["status"] == "Pendente"


def test_atendimento_sem_cliente(banco_temporario):
    with pytest.raises(ValueError):
        database.cadastrar_atendimento(
            9999, "Colar Delicado", "2026-11-07"
        )


def test_atualizar_status(banco_temporario):
    cliente_id = database.cadastrar_cliente(
        "Cliente Exemplo", "WhatsApp"
    )

    atendimento_id = database.cadastrar_atendimento(
        cliente_id,
        "Brinco de Zircônia",
        "2026-11-07"
    )

    database.atualizar_status(
        atendimento_id, "Concluído"
    )

    atendimentos = database.listar_atendimentos()

    assert atendimentos[0]["status"] == "Concluído"


def test_status_invalido(banco_temporario):
    with pytest.raises(ValueError):
        database.atualizar_status(9999, "Cancelado")
