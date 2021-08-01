from app import app, db
from app.models import Produto
from flask import render_template, redirect, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/cadastrar/novo', methods=['POST'])
def cadastrar_novo_produto():
    nome_produto = request.form['nome']
    if nome_produto:
        novo_produto = Produto(nome=nome_produto)
        try:
            db.session.add(novo_produto)
            db.session.commit()
            print(f'{nome_produto} cadastrado com sucesso')
        except Exception:
            print(f'Erro: {nome_produto} não foi cadastrado')
    return redirect('/cadastrar')
