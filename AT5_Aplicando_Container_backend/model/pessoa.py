from flask_restful import fields
from helpers.database import db
from sqlalchemy.types import String



pessoa_fields = {
    'id': fields.Integer,
    'nome': fields.String(),
    'email': fields.String(),
    'senha': fields.String(),
    'telefone': fields.String()
}

class Pessoa(db.Model):

    __tablename__ = "pessoa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, unique=True, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico
    
    tipo = db.Column('tipo', String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'pessoa',
        'polymorphic_on': 'tipo'
    }

    def __init__(self, nome, email, senha, telefone):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.excluido = False

    def __repr__(self):
        return f'<Pessoa {self.nome}, {self.email}, {self.telefone}>'
