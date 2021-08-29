import os

basedir = os.path.abspath(os.path.dirname(__file__))

EXTENSOES_PERMITDAS = {'png', 'jpg', 'jpeg', 'gif'}


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'catalogo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta'
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'imagens')
