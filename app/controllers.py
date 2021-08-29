import logging
import os

from flask_login.utils import login_required
from app import app, db
from config import EXTENSOES_PERMITDAS
from flask import render_template, redirect, request
from app.models import Processadores, Produtos, ImagensProdutos, HDs, Usuarios
from app.forms import ProcessadoresForm, HDsForm, LoginForm
from flask_login import current_user, login_user, logout_user

forms = {
    'processadores': ProcessadoresForm,
    'hds': HDsForm
}

produtos = {
    'processadores': Processadores,
    'hds': HDs
}


def extensao(nome_arquivo):
    return nome_arquivo.rsplit('.', 1)[1].lower()


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
@login_required
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
                return redirect(f'/admin/cadastrar/imagens/{novo_produto.id}')
    return redirect('/')


@app.route('/admin/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    try:
        produto_id = int(id)
    except Exception:
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
        return redirect(f'/admin/cadastrar/imagens/{produto_id}')
    return redirect('/')


@app.route('/admin/remover/<id>')
@login_required
def remover(id):
    try:
        produto_id = int(id)
    except Exception:
        return redirect('/')
    produto = Produtos.query.filter(
        Produtos.id == produto_id
    ).first()
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect('/')


@app.route('/admin/cadastrar/imagens/<id>')
@login_required
def cadastrar_imagens(id):
    produto = Produtos.query.join(ImagensProdutos, isouter=True).filter(
        Produtos.id == id
    ).first()
    if produto:
        padrao = ['img_padrao.png', 'img_padrao.png']
        imagens_existentes = [imagem.caminho for imagem in produto.imagens]
        imagens = (imagens_existentes + padrao)[:len(padrao)]
        nome_imagem = produto.modelo.lower()
        return render_template('cadastrar_imagens.html', imagens=imagens, id=id, nome_imagem=nome_imagem)
    return redirect(request.referrer)


@app.route('/upload', methods=['POST'])
def upload():
    if 'arquivo' not in request.files:
        return redirect(request.referrer)
    arquivo = request.files['arquivo']
    if not arquivo.filename:
        return redirect(request.referrer)
    imagem_num = int(request.form['imagem_num'])
    produto_id = int(request.form['produto_id'])
    extensao_arquivo = extensao(arquivo.filename)
    if extensao_arquivo not in EXTENSOES_PERMITDAS:
        return redirect(request.referrer)
    nome_arquivo = f'{request.form["nome_imagem"]}_{imagem_num}.{extensao_arquivo}'
    arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
    produto = Produtos.query.join(ImagensProdutos, isouter=True).filter(
        Produtos.id == produto_id
    ).first()
    if produto:
        quantidade_imagens = len(produto.imagens)
        if imagem_num >= quantidade_imagens:
            imagem = ImagensProdutos()
            imagem.caminho = nome_arquivo
            imagem.produto_id = produto_id
            db.session.add(imagem)
            db.session.commit()
        else:
            imagem = produto.imagens[imagem_num]
            imagem.caminho = nome_arquivo
            imagem.produto_id = produto_id
    return redirect(request.referrer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if request.method == 'POST' and form.validate():
        usuario = Usuarios.query.filter_by(nome=form.nome.data).first()
        if not usuario or not usuario.verifica_senha(form.senha.data):
            return redirect('/')
        login_user(usuario, remember=form.lembrar_me.data)
        return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/produtos/<tipo_produto>')
def visualizar_categoria(tipo_produto):
    if tipo_produto in produtos:
        itens = Produtos.query.filter_by(type=tipo_produto).all()
        return render_template('visualizar_categoria.html', itens=itens)
    return redirect('/')
