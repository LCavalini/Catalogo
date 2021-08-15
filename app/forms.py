from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

class ProdutosForm(FlaskForm):
    nome = StringField('Nome: ')
    preco = StringField('Preço: ')
    quantidade = StringField('Quantidade: ')
    marca = StringField('Marca: ')
    modelo = StringField('Modelo: ')
    garantia = StringField('Garantia: ')
    enviar = SubmitField('Gravar')


class ProcessadoresForm(ProdutosForm):
    nucleos = StringField('Núcleos: ')
    threads = StringField('Threads: ')
    frequencia_base = StringField('Frequência base: ')
    frequencia_turbo = StringField('Frequência turbo: ')
    tdp = StringField('TDP: ')
    soquete = StringField('Soquete: ')
    litografia = StringField('Litografia: ')
    video = StringField('Vídeo integrado: ')
    tecnologias = TextAreaField('Tecnologias: ')


class HDsForm(ProdutosForm):
    capacidade = StringField('Capacidade: ')
    interface = StringField('Interface: ')
    rpm = StringField('RPM: ')
    formato = StringField('Formato: ')
    cache = StringField('Cache: ')
