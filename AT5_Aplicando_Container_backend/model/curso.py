from flask_restful import fields
from helpers.database import db
from model.instituicao import Instituicao, instituicao_fields



curso_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'instituicao': fields.Nested(instituicao_fields)

}


class Curso(db.Model):

    __tablename__ = "curso"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico

    instituicao_id = db.Column(db.Integer, db.ForeignKey('instituicao.id'), nullable=False)
    instituicao = db.relationship('Instituicao', backref='cursos')

    def __init__(self, nome, instituicao):
        self.nome = nome
        self.instituicao = instituicao
        self.excluido = False


    def __repr__(self):
        return f'<Curso {self.nome}>'

