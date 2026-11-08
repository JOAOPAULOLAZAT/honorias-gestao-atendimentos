
from flask import Flask, render_template_string, request, redirect, url_for
import database

app = Flask(__name__)

database.criar_tabelas()

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Honórias | Gestão de Atendimentos</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            color: #222;
        }
        header {
            background: #171717;
            color: white;
            padding: 24px;
            text-align: center;
        }
        header h1 { margin: 0; }
        header p { margin-bottom: 0; }
        main {
            max-width: 1050px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 22px;
            box-shadow: 0 2px 8px #00000012;
        }
        h2 { color: #9b1735; }
        label {
            display: block;
            margin: 12px 0 6px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            border: 1px solid #888;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            background: #9b1735;
            color: white;
            border: 0;
            padding: 14px 20px;
            margin-top: 14px;
            border-radius: 6px;
            cursor: pointer;
            min-height: 44px;
            font-size: 16px;
        }
        button:hover { background: #751029; }
        button:focus-visible, input:focus-visible,
        select:focus-visible {
            outline: 3px solid #245bdb;
            outline-offset: 3px;
        }
        .registro {
            padding: 15px 0;
            border-bottom: 1px solid #ddd;
        }
        .registro:last-child { border-bottom: 0; }
        .status { font-weight: bold; }
        .erro { color: #9b1735; font-weight: bold; }
    </style>
</head>
<body>
<header>
    <h1>HONÓRIAS</h1>
    <p>Gestão de Clientes e Atendimentos</p>
</header>

<main>
    <section class="card">
        <h2>Cadastrar cliente</h2>
        <form action="/clientes" method="post">
            <label for="nome">Nome do cliente *</label>
            <input id="nome" name="nome" required>

            <label for="telefone">Telefone (opcional)</label>
            <input id="telefone" name="telefone">

            <label for="canal">Canal de contato *</label>
            <select id="canal" name="canal" required>
                <option value="">Selecione</option>
                <option>WhatsApp</option>
                <option>Instagram</option>
            </select>

            <button type="submit">Cadastrar cliente</button>
        </form>
    </section>

    <section class="card">
        <h2>Registrar atendimento</h2>
        <form action="/atendimentos" method="post">
            <label for="cliente_id">Cliente *</label>
            <select id="cliente_id" name="cliente_id" required>
                <option value="">Selecione</option>
                {% for cliente in clientes %}
                <option value="{{ cliente.id }}">
                    {{ cliente.nome }}
                </option>
                {% endfor %}
            </select>

            <label for="produto">Produto de interesse *</label>
            <input id="produto" name="produto" required>

            <label for="data">Data *</label>
            <input id="data" name="data" type="date" required>

            <button type="submit">Registrar atendimento</button>
        </form>
    </section>

    <section class="card">
        <h2>Atendimentos registrados</h2>
        {% for atendimento in atendimentos %}
        <div class="registro">
            <strong>{{ atendimento.cliente }}</strong>
            <p>Produto: {{ atendimento.produto_interesse }}</p>
            <p class="status">
                Situação: {{ atendimento.status }}
            </p>
            <form action="/status" method="post">
                <input type="hidden" name="id"
                       value="{{ atendimento.id }}">
                <label for="status-{{ atendimento.id }}">
                    Atualizar situação
                </label>
                <select id="status-{{ atendimento.id }}"
                        name="status">
                    {% for opcao in
                       ['Pendente', 'Em andamento', 'Concluído'] %}
                    <option value="{{ opcao }}"
                        {% if opcao == atendimento.status %}
                        selected
                        {% endif %}>
                        {{ opcao }}
                    </option>
                    {% endfor %}
                </select>
                <button type="submit">Salvar situação</button>
            </form>
        </div>
        {% else %}
        <p>Nenhum atendimento registrado.</p>
        {% endfor %}
    </section>
</main>
</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(
        HTML,
        clientes=database.listar_clientes(),
        atendimentos=database.listar_atendimentos()
    )


@app.route("/clientes", methods=["POST"])
def cadastrar_cliente():
    database.cadastrar_cliente(
        request.form.get("nome", ""),
        request.form.get("canal", ""),
        request.form.get("telefone") or None
    )
    return redirect(url_for("inicio"))


@app.route("/atendimentos", methods=["POST"])
def cadastrar_atendimento():
    database.cadastrar_atendimento(
        int(request.form["cliente_id"]),
        request.form["produto"],
        request.form["data"]
    )
    return redirect(url_for("inicio"))


@app.route("/status", methods=["POST"])
def atualizar_status():
    database.atualizar_status(
        int(request.form["id"]),
        request.form["status"]
    )
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=False)
