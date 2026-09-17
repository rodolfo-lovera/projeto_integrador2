import os
from flask import Flask, jsonify

def create_app():
    """ Cria, configura e retorna a instância da aplicação Flask.
    """
    
    app = Flask(__name__)
    
    # Carregamento das configurações básicas
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY","chave-padrao-desenvolvimento")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACJ_MODIFICATIONS"] = False
    
    # rota de teste para conectividade
    @app.route("/")
    def index():
        return jsonify({
            "projeto": "IceWebCream 2.0",
            "status": "Aplicação rodando no conteiner Docker!",
            "ambiente":"Desenvolvimento Local"
        })
    
    return app