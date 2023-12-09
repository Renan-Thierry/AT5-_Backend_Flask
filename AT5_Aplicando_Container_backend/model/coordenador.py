from flask_restful import fields
from helpers.database import db
from model.professor import Professor
from model.curso import Curso, curso_fields

coordenador_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'senha': fields.String,
    'telefone': fields.String,
    'disciplina': fields.String,
    'registrodeTrabalho': fields.String,
    'curso': fields.Nested(curso_fields)
}

class Coordenador(Professor):
    __tablename__ = 'coordenador'
    id = db.Column(db.Integer, db.ForeignKey('professor.id'), primary_key=True)
    registrodeTrabalho = db.Column(db.String, nullable=False)
    excluido_coordenador = db.Column(db.Boolean, default=False)  # Delete lógico


    __mapper_args__ = {
        'polymorphic_identity': 'coordenador'
    }

    def __init__(self, nome, email, senha, telefone, disciplina, curso, registrodeTrabalho):
        super().__init__(nome, email, senha, telefone, disciplina, curso)
        self.registrodeTrabalho = registrodeTrabalho
        self.excluido_coordenador = False
    
    def __repr__(self):
        return f'<Coordenador {self.registrodeTrabalho}>'
