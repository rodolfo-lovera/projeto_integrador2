from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def dashboard():
    """ Entrega a tela principal com o painel de produtos e controle de estoque. """
    return render_template("estoque/index.html")