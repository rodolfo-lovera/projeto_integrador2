from app import db
from app.models.estoque import Produto, Estoque

def test_calculo_saldo_apos_entrada(app):
    """Testa adição de saldo"""
    with app.app_context():
        prod = Produto(sku="COR-01", nome="Morango Congelado", estoque_minimo=5.0, categoria_id=1)
        est = Estoque(produto=prod, quantidade_atual=10.0)
        db.session.add_all([prod, est])
        db.session.commit()
        
        # Calculo para Entrada de itens no estoque
        quantidade_entrada = 5.0
        est.quantidade_atual += quantidade_entrada
        db.session.commit()
        
        assert est.quantidade_atual == 15.0
    
def test_gatilho_alerta_estoque_minimo(app):
    """Testa alerta e gatilho de estoque baixo (quantidade <= estoque_minimo)"""
    with app.app_context():
        prod = Produto(sku="POL-01", nome="Polpa de Maracujá", estoque_minimo=10.0, categoria_id=1)
        est = Estoque(produto=prod, quantidade_atual=15.0)
        db.session.add_all([prod, est])
        db.session.commit()
        
        # Saldo maior não precisa de reposição
        assert prod.to_dict()["precisa_reposicao"] is False
        
        # Saldo igual ao mínimo para ativar alerta (teste de borda)
        est.quantidade_atual = 10.0
        db.session.commit()
        assert prod.to_dict()["precisa_reposicao"] is True
        
        # Saldo abaixo do mínimo
        est.quantidade_atual = 4.0
        db.session.commit()
        assert prod.to_dict()["precisa_reposicao"] is True