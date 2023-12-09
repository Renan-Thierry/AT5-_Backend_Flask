from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.periodo import Periodo, periodo_fields
from model.curso import Curso, curso_fields

aluno_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'senha': fields.String,
    'telefone': fields.String,
    'matricula': fields.String,
    'periodo': fields.Nested(periodo_fields),
    'curso': fields.Nested(curso_fields)
}

class Aluno(Pessoa):
    __tablename__ = 'aluno'
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), primary_key=True)
    matricula = db.Column(db.String, nullable=False)
    excluido_aluno = db.Column(db.Boolean, default=False)  # Delete lógico

    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    periodo = db.relationship('Periodo', backref='alunos')
    curso = db.relationship('Curso', backref='alunos')

    __mapper_args__ = {
        'polymorphic_identity': 'aluno'
    }

    def __init__(self, nome, email, senha, telefone, matricula, periodo, curso):
        super().__init__(nome, email, senha, telefone)
        self.matricula = matricula
        self.periodo = periodo
        self.curso = curso
        self.excluido_aluno = False

    def __repr__(self):
        return f'<Aluno {self.matricula}>'
