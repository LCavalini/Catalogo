from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired


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


class LoginForm(FlaskForm):
    nome = StringField('Nome de usuário: ', validators=[DataRequired()])
    senha = PasswordField('Senha: ', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar-me ')
    enviar = SubmitField('Entrar')
