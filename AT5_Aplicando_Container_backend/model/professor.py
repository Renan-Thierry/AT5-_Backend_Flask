from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.curso import Curso, curso_fields

professor_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'senha': fields.String,
    'telefone': fields.String,
    'disciplina': fields.String,
    'curso': fields.Nested(curso_fields)
   
}
class Professor(Pessoa):
    __tablename__ = 'professor'
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), primary_key=True)
    disciplina = db.Column(db.String, nullable=False)
    excluido_professor = db.Column(db.Boolean, default=False)  # Delete lógico

    curso_professor_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    curso = db.relationship('Curso', backref='professores')

    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }

    def __init__(self, nome, email, senha, telefone, disciplina, curso):
        super().__init__(nome, email, senha, telefone)
        self.disciplina = disciplina
        self.curso = curso
        self.excluido_professor = False
    
    def __repr__(self):
        return f'<Professor {self.disciplina}>'
