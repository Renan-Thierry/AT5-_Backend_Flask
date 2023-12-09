from flask_restful import fields
from helpers.database import db
from model.endereco import Endereco, endereco_fields

instituicao_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'endereco': fields.Nested(endereco_fields)
}

class Instituicao(db.Model):
    __tablename__ = "instituicao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico

    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=False)
    endereco = db.relationship('Endereco', backref='instituicoes')

    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.excluido = False

    def __repr__(self):
        return f'<Instituicao {self.nome}>'
