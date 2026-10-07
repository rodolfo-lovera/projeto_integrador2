from flask import Blueprint, jsonify, request
from app import db
from app.models import Categoria, Produto, Estoque, Movimentacao

api_bp = Blueprint("api", __name__, url_prefix="/api")

# --- Categorias ---
@api_bp.route("/categorias", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return jsonify([cat.to_dict() for cat in categorias]), 200

# --- Produtos ---
@api_bp.route("/produtos",methods=["GET"])
def listar_produtos():
    produtos = Produto.query.filter_by(ativo=True).all()
    return jsonify([p.to_dict() for p in produtos]), 200

@api_bp.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.get_json() or {}
    
    sku = dados.get("sku")
    nome = dados.get("nome")
    categoria_id = dados.get("categoria_id")
    
    if not sku or not nome or not categoria_id:
        return jsonify({"erro": "Campos obrigatórios: sku, nome e categoria_id"}), 400
    
    if Produto.query.filter_by(sku=sku).first():
        return jsonify({"erro": f"O SKU '{sku}' já existe no catálogo"}), 409
    
    novo_produto = Produto(
        sku=sku,
        nome=nome,
        unidade_medida=dados.get("unidade_medida","UN"),
        estoque_minimo=float(dados.get("estoque_minimo",5.0)),
        preco_custo=float(dados.get("preco_custo",0,0)),
        categoria_id=int(categoria_id)
    )
    
    # Cria o registro inicial com saldo zero
    estoque_inicial = Estoque(produto=novo_produto, quantidade_atual=0.0)
    
    db.session.add(novo_produto)
    db.session.add(estoque_inicial)
    db.session.commit()
    
    return jsonify(novo_produto.to_dict()),201

# --- Movimentações de estoque (Entradas e Saídas) ---
def registrar_movimentacao():
    dados = request.get_json() or {}
    
    produto_id = dados.get("produto_id")
    tipo = dados.get("tipo")
    try:
        quantidade = float(dados.get("quantidade",0))
    except (ValueError, TypeError):
        return jsonify({"erro": "Quantidade informada deve ser numérico"}),400
    
    motivo = dados.get
    
    if not produto_id or tipo not in ["ENTRADA","SAIDA"] or quantidade <= 0:
        return jsonify({"erro": "Quantidade informada deve ser numérico"}), 400

    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    
    estoque = Estoque.query.filter_by(produto_id=produto.id).first()
    if not estoque:
        estoque = Estoque(produto_id=produto.id, quantidade_atual=0.0)
        db.session.add(estoque)
    
    # Regra de negócio de auditoria e saldo
    if tipo == "ENTRADA":
        estoque.quantidade_atual += quantidade
    elif tipo == "SAIDA":
        if estoque.quantidade_atual < quantidade:
            return jsonify({
                "erro":f"Saldo insuficiente. Quantidade disponível: {estoque.quantidade_atual}"                
            }), 400
        estoque.quantidade_atual -= quantidade
    
    nova_mov = Movimentacao(
        produto_id=produto.id,
        tipo=tipo,
        quantidade=quantidade,
        motivo=motivo
    )
    
    db.session.add(nova_mov)
    db.session.commit()
    
    return jsonify({
        "mensagem": f"Movimentação de {tipo} realizada com sucesso!",
        "produto": produto.nome,
        "saldo_atual":estoque.quantidade_atual,
        "precisa_reposicao": produto.to_dict()["precisa_reposicao"]
    }), 200