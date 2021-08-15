from app import app, db
import logging
from flask import render_template, redirect, request
from app.models import Processadores, Produtos, ImagensProdutos, HDs
from app.forms import ProcessadoresForm, HDsForm

forms = {
    'processadores': ProcessadoresForm,
    'hds': HDsForm
}

produtos = {
    'processadores': Processadores,
    'hds': HDs
}

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
                            especificacoes=especificacoes, imagens=imagens, tipo=tipo, id=id)


@app.route('/admin/cadastrar/', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        if 'tipo' in request.args:
            tipo = request.args['tipo']
            if tipo in forms:
                form = forms[tipo]()
                return render_template('cadastrar.html', form=form, tipo=tipo, acao='cadastrar')
    if request.method == 'POST':
        if 'tipo' in request.form:
            tipo = request.form['tipo']
            if tipo in produtos:
                dados = {chave: valor for chave, valor in request.form.items() 
                        if chave not in ('enviar', 'tipo', 'csrf_token')}
                if 'tecnologias' in dados:
                    dados['tecnologias'] = dados['tecnologias'].encode()
                novo_produto = produtos[tipo](**dados)
                db.session.add(novo_produto)
                db.session.commit()
    return redirect('/')

@app.route('/admin/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    try:
        produto_id = int(id)
    except:
        return redirect('/')
    if request.method == 'GET':
        produto = Produtos.query.join(ImagensProdutos, isouter=True).filter(
            Produtos.id == id
        ).first()
        if produto:
            tipo = produto.type
            if tipo in forms:
                form = forms[tipo](obj=produto)
                if hasattr(form, 'tecnologias'):
                    if form.tecnologias.data:
                        form.tecnologias.data = form.tecnologias.data.decode('utf-8')
                return render_template('cadastrar.html', form=form, tipo=tipo, acao='editar', id=produto_id)
    if request.method == 'POST':
        produto = Produtos.query.filter(
            Produtos.id == produto_id
        ).first()
        if produto:
            dados = {chave: valor for chave, valor in request.form.items() 
                    if chave not in ('enviar', 'tipo', 'csrf_token')}
            if 'tecnologias' in dados:
                dados['tecnologias'] = dados['tecnologias'].encode()
            for coluna, valor in dados.items():
                setattr(produto, coluna, valor)
            db.session.commit()
    return redirect('/')


@app.route('/admin/remover/<id>')
def remover(id):
    try:
        produto_id = int(id)
    except:
        return redirect('/')
    produto = Produtos.query.filter(
        Produtos.id == produto_id
    ).first()
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect('/')    