from datetime import datetime
from app import db

class Categoria(db.Model):
    __tablename__ = "categorias"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=True)
    
    # Relacionamento 1:N com Produtos
    produtos = db.relationship("Produto", backref="categoria", lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }

class Produto(db.Model):
    __tablename__ = "produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(120), nullable=False)
    unidade_medida = db.Column(db.String(20), nullable=False, default='UN')
    estoque_minino = db.Column(db.Float, nullable=False, default=5.0)
    preco_custo = db.Column(db.Float, nullable=True, default=0.0)
    ativo = db.Column(db.Boolean, default=True)
    
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    
    # Relacionamento 1:1 com estoque e 1:N com Movimentacoes
    estoque = db.relationship("Estoque", backref="produto", uselist=False, cascade="all, delete-orphan")
    movimentacoes = db.relationship("Movimentacao", backref="produto", lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "nome": self.nome,
            "unidade_medida":self.unidade_medida,
            "estoque_minimo":self.estoque_minino,
            "preco_custo": self.preco_custo,
            "ativo": self.ativo,
            "categoria_id": self.categoria_id,
            "quantidade_atual": self.estoque.quantidade_atual if self.estoque else 0.0,
            "precisa_reposicao": (self.estoque.quantidade_atual <= self.estoque_minimo) if self.estoque else True
        }

class Estoque(db.Model):
    __tablename__ = "estoque"
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False, unique=True)
    quantidade_atual = db.Column(db.Float, nullable=False, default=0.0)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id":self.id,
            "produto_id": self.produto_id,
            "quantidade_atual": self.quantidade_atual,
            "ultima_atualizacao": self.ultima_atualizacao.isoformat() if self.ultima_atualizacao else None
        }

class Movimentacao(db.Model):
    __tablename__ = "movimentacoes"
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    motivo = db.Column(db.String(150), nullable=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "tipo": self.tipo,
            "quantidade": self.quantidade,
            "motivo": self.motivo,
            "data_hora": self.data_hora.isoformat() if self.data_hora else None
        }
    