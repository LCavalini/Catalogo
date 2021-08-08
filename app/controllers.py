from app import app, db
import logging
from flask import render_template, redirect, request
from app.models import Produtos, ImagensProdutos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/<produto_id>')
def produto(produto_id):
    try:
        id = int(produto_id)
    except Exception:
        logging.warning(f'O id ({produto_id}) do produto é inválido')
        return redirect('/')
    resultado = Produtos.query.join(ImagensProdutos, isouter=True).filter(
        Produtos.id == id
    ).first()
    if not resultado:
        logging.warning(f'O id ({id}) do produto não foi encontrado')
        return redirect('/')
    nome = resultado.nome
    preco = f'R$ {resultado.preco}'
    quantidade = resultado.quantidade
    tipo = resultado.type
    especificacoes = resultado.especificacoes
    imagens = []
    if resultado.imagens:
        imagens = [f'static/imagens/{imagem.caminho}' for imagem in resultado.imagens]
    return render_template('produto.html', nome=nome, preco=preco, quantidade=quantidade,
                            especificacoes=especificacoes, imagens=imagens, tipo=tipo)


@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/cadastrar/novo')
def cadastrar_novo_produto():
    """
    nome_produto = request.args.get('nome')
    if nome_produto:
        novo_produto = Produto(nome=nome_produto)
        try:
            db.session.add(novo_produto)
            db.session.commit()
            print(f'{nome_produto} cadastrado com sucesso')
        except Exception:
            print(f'Erro: {nome_produto} não foi cadastrado')
    """
    return redirect('/cadastrar')
