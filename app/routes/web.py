from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def index():
    """Painel principal com visão geral do estoque."""
    return render_template("estoque/index.html")

@web_bp.route("/cadastro")
def cadastro():
    """Tela de cadastro de novos produtos."""
    return render_template("estoque/cadastro_produto.html")

@web_bp.route("/movimentacao")
def movimentacao():
    """Tela para registrar entradas, saídas ou ajustes de estoque."""
    return render_template("estoque/movimentacao.html")

@web_bp.route("/compras")
def compras():
    """Tela de sugestão e relatório de reposição."""
    return render_template("estoque/compras.html")