from app import db
from app.models.estoque import Produto, Estoque

def test_criar_produto_sucesso_status_201(client):
    """Testa o cadastro de produto com retorno HTTP"""
    payload = {
        "sku": "LEI-01",
        "nome": "Leite Integral 1L",
        "categoria_id": 1,
        "unidade_medida": "L",
        "estoque_minimo": 8.0,
        "preco_custo": 4.50
    }
    resposta =client.post("/api/produtos", json=payload)
    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados["sku"] == "LEI-01"
    assert dados["quantidade_atual"] == 0.0

def test_criar_produto_duplicador_status_409(client):
    """Tenta a tentativa de cadastrar o mesmo SKU, esperando HTTP de conflito"""
    payload = {
        "sku": "CHO-01",
        "nome": "Chocolate em pó",
        "categoria_id": 1
    }
    # Cadastro
    client.post("/api/produtos", json=payload)
    
    # Cadastro duplicado
    resposta_duplicada = client.post("/api/produtos", json=payload)
    assert resposta_duplicada.status_code == 409
    assert "já existe" in resposta_duplicada.get_json()["erro"].lower()

def test_movimentacao_saida_saldo_insuficiente_status_400(client, app):
    """Testa tentativa de saída maior que estoque, esperando HTTP Bad request"""
    with app.app_context():
        prod = Produto(sku="BAU-01", nome="Baunilha", estoque_minimo=2.0, categoria_id=1)
        est = Estoque(produto=prod, quantidade_atual=3.0)
        db.session.add_all([prod,est])
        db.session.commit()
        prod_id = prod.id
    
    # Retirando quantidade maior que o estoque
    payload = {
        "produto_id": prod_id,
        "tipo": "SAIDA",
        "quantidade": 10.0,
        "motivo": "Uso na produção"
    }
    resposta = client.post("/api/movimentacoes",json=payload)
    assert resposta.status_code == 400
    assert "Saldo insuficiente" in resposta.get_json()["erro"]
    
def test_movimentacao_ajuste_estoque_status_200(client, app):
    """Testa operação de ajuste de prateleira, HTTP ok"""
    with app.app_context():
        prod = Produto(sku="COP-01", nome="Copo 200ml", estoque_minimo=50.0, categoria_id=1)
        est = Estoque(produto=prod, quantidade_atual=10.0)
        db.session.add_all([prod, est])
        db.session.commit()
        prod_id = prod.id
    
    # Insere quantidade para maior que minimo
    payload = {
        "produto_id": prod_id,
        "tipo": "AJUSTE",
        "quantidade": 100.,
        "motivo": "Contagem física do estoque"
    }
    resposta = client.post("/api/movimentacoes", json=payload)
    assert resposta.status_code == 200
    assert resposta.get_json()["saldo_atual"] == 100.0