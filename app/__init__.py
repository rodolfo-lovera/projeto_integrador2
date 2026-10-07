import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config_by_name, DevelopmentConfig

# Instancia a extensão do ORM sem vincular n\nhuma aplicação ainda
db = SQLAlchemy()

def create_app(config_name=None):
    """ Cria a instância Flask, carrega as configurações e acopla as extensões """
    app = Flask(__name__)
    
    env_name = config_name or os.getenv("FLAK_ENV", "development")
    config_class = config_by_name.get(env_name, DevelopmentConfig)
    app.config.from_object(config_class)
    
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"
    
    # Inicializa o banco de dados com a configuração carregada
    db.init_app(app)
    
    # Registro dos Blueprint da aplicação
    from app.routes import web_bp, api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    
    return app