from flask_restful import fields
from helpers.database import db

controleAlunos_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'numero': fields.String,
    'matricula': fields.String,
    'curso': fields.String
}

class ControleAluno(db.Model):
    __tablename__ = "controleAluno"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    matricula = db.Column(db.String, nullable=False)
    curso = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico

    def __init__(self, nome, email, numero, matricula, curso):
        self.nome = nome
        self.email = email
        self.numero = numero
        self.matricula = matricula
        self.curso = curso
        self.excluido = False

    def __repr__(self):
        return f'<ControleAluno {self.nome}, {self.email}, {self.matricula}, {self.numero}, {self.curso}>'
