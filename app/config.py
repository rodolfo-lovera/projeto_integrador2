import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent.parent
load_dotenv(basedir / ".env")

class Config:
    """ Configurações base compartilhadas entre ambiente"""
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-temporaria-desenvolvimento-pi2")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Captura a URL do banco (PostgreSQL local do Docker, Supabase)
    _db_url = os.getenv("DATABASE_URL")
    
    # Ajuste técnico para compativilidade com o SQLAchemy 2.0+
    if _db_url:
        if _db_url and _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql+psycop2://",1)
        elif _db_url.startswith("postgresql://") and not _db_url.startswith("postgresql+"):
            _db_url = _db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    SQLALCHEMY_DATABASE_URI = _db_url or "sqlite:///temp.db"

class DevelopmentConfig(Config):
    """ Ambiente de desenvolvimento local"""
    DEBUG = True

class ProductionConfig(Config):
    """ Ambiente de produção (nuvem) """
    DEBUG = False

# Dicionário mapeador de ambientes
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}