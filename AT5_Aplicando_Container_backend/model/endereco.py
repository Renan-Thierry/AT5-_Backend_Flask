from flask_restful import fields
from helpers.database import db

endereco_fields = {
    'id': fields.Integer,
    'rua': fields.String,
    'bairro': fields.String,
    'cep': fields.String,
    'numero': fields.String,
    'complemento': fields.String
}

class Endereco(db.Model):
    __tablename__ = "endereco"

    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String, nullable=False)
    bairro = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    complemento = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico

    def __init__(self, rua, bairro, cep, numero, complemento):
        self.rua = rua
        self.bairro = bairro
        self.cep = cep
        self.numero = numero
        self.complemento = complemento
        self.excluido = False

    def __repr__(self):
        return f'<Endereco {self.rua}, {self.bairro}, {self.cep}, {self.numero}, {self.complemento}>'
