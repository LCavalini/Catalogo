from sqlalchemy.orm import relationship
from app import db

class Produtos(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), unique=True)
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    garantia = db.Column(db.Integer)
    quantidade = db.Column(db.Integer)
    preco = db.Column(db.String(20))
    img_principal = db.Column(db.String(300))
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'produtos',
        'polymorphic_on': type
    }
    imagens = relationship('ImagensProdutos')

    @property
    def especificacoes(self):
        return {
            'Marca:': self.marca,
            'Modelo:' : self.modelo,
            'Garantia:': f'{self.garantia} meses'
        }


class Processadores(Produtos):
    __tablename__ = 'processadores'
    id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    nucleos = db.Column(db.Integer)
    threads = db.Column(db.Integer)
    frequencia_base = db.Column(db.Integer)
    frequencia_turbo = db.Column(db.Integer)
    tdp = db.Column(db.Integer)
    soquete = db.Column(db.String(20))
    litografia = db.Column(db.String(20))
    tecnologias = db.Column(db.LargeBinary)
    video = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'processadores',
    }

    @property
    def especificacoes(self):
        return {
            'Marca:': self.marca,
            'Modelo:' : self.modelo,
            'Garantia:': f'{self.garantia} meses',
            'Núcleos:' : self.nucleos,
            'Threads:' : self.threads,
            'Frequência base:' : f'{self.frequencia_base/1000:.1f} GHz',
            'Frequência turbo:': f'{self.frequencia_turbo/1000:.1f} GHz',
            'TDP:' : f'{self.tdp} W',
            'Soquete:' : self.soquete,
            'Litografia:' : self.litografia,
            'Tecnologias:' : self.tecnologias.decode('utf-8').split('\n'),
            'Vídeo integrado:' : self.video
        }
    
class HDs(Produtos):
    __tablename__ = 'hds'
    id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    capacidade = db.Column(db.Integer)
    interface = db.Column(db.String(20))
    rpm = db.Column(db.Integer)
    cache = db.Column(db.Integer)
    formato = db.Column(db.Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'hds',
    }

    @property
    def especificacoes(self):
        unidade_capacidade = 'TB' if self.capacidade >= 1024 else 'GB'
        capacidade = self.capacidade / 1024 if self.capacidade >= 1024 else self.capacidade
        return {
            'Marca:': self.marca,
            'Modelo:' : self.modelo,
            'Garantia:': f'{self.garantia} meses',
            'Capacidade:' : f'{capacidade} {unidade_capacidade}',
            'Interface:' : self.interface,
            'RPM:' : self.rpm,
            'Formato:' : f'{self.formato / 10:.1f}"',
            'Cache:' : f'{self.cache} MB'
        }


class ImagensProdutos(db.Model):
    __tablename__ = 'imagens_produtos'
    id = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(300))
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'))
