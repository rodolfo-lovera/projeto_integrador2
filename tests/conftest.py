import sys
from pathlib import Path
import pytest
from sqlalchemy.pool import StaticPool

# Adiciona o diretório raiz (/app) ao path de importação
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app, db
from app.config import Config, config_by_name
from app.models.estoque import Categoria, Fornecedor, Produto, Estoque

# 1. Cria a configuração de testes isolada em memória
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Garante que todas as conexões do teste usem a mesma instância de memória RAM
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False}
    }

# Registra o perfil de testes no mapeador da aplicação
config_by_name["testing"] = TestingConfig


@pytest.fixture
def app():
    """Cria a aplicação já apontando para o banco em memória e prepara os dados."""
    # 2. Instancia a aplicação passando explicitamente o perfil de teste
    app = create_app("testing")

    with app.app_context():
        # Cria as tabelas na memória RAM
        db.create_all()

        # Insere os dados base para satisfazer as chaves estrangeiras
        cat = Categoria(nome="Insumos", descricao="Materia-prima")
        forn = Fornecedor(nome="Fornecedor Teste", telefone="11999887766")
        db.session.add_all([cat, forn])
        db.session.commit()

        yield app

        # Limpeza ao término de cada teste
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente HTTP simulado para testes de endpoints de API."""
    return app.test_client()