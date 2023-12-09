from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.professor import Professor, professor_fields
from model.curso import Curso, curso_fields
from sqlalchemy.exc import IntegrityError
from model.pessoa import Pessoa



parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('disciplina', type=str, help='Problema na conversão da disciplina')

parser.add_argument('curso', type=dict, required=True)

class ProfessorResource(Resource):
    @marshal_with(professor_fields)
    def get(self, professor_id=None):
        log.info("Get - Professores")        
        professores = Professor.query.filter_by(excluido_professor=False).all()
        return professores, 200

    def post(self):
        log.info("Post - Professores")
        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        disciplina = args['disciplina']

        # Extract Curso data from the request JSON
        curso_professor_id = args['curso']['id']

        # Fetch Instituicao and Curso from the database
        curso = Curso.query.filter_by(id=curso_professor_id, excluido=False).first()

        if not curso:
            return {'message': 'Invalid Curso'}, 400
        
        try:
            # Check if email or senha already exists
            # Check if email already exists
            if Pessoa.query.filter(Professor.email == email).first():
                return {'message': 'Email already exists'}, 400

            # Check if senha already exists
            if Pessoa.query.filter(Professor.senha == senha).first():
                return {'message': 'Senha already exists'}, 400

            professor = Professor(nome=nome, email=email, senha=senha, telefone=telefone, disciplina=disciplina, curso=curso)
            db.session.add(professor)
            db.session.commit()

            return {'message': 'Professor created successfully'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Email or senha already exists'}, 400

    
class ProfessoresResource(Resource):

    def get(self, professor_id):
        log.info("Get - Professores")        
        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()

        if (professor is not None):
            return marshal(professor, professor_fields), 201
        else:
            return {'message': 'Professor not found'}, 404
        
    def put(self, professor_id):
        log.info("Put - Professores")

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        disciplina = args['disciplina']

        # Fetch the Professor from the database
        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()


        if not professor:
            return {'message': 'Professor not found'}, 404
        
        email = args.get('email')
        senha = args.get('senha')

        # Verificar se o email já existe
        if email and Pessoa.query.filter_by(email=email).filter(Professor.id != professor_id).first():
            return {'message': 'Email already exists'}, 400

        # Verificar se a senha já existe
        if senha and Pessoa.query.filter_by(senha=senha).filter(Professor.id != professor_id).first():
            return {'message': 'Senha already exists'}, 400

        # Update Professor attributes based on the request args
        if nome:
            professor.nome = nome
        if email:
            professor.email = email
        if senha:
            professor.senha = senha
        if telefone:
            professor.telefone = telefone
        if disciplina:
            professor.disciplina = disciplina

        curso_professor_id = args['curso'].get('id')
        if curso_professor_id:
            curso = Curso.query.get(curso_professor_id)
            if not curso:
                return {'message': 'Invalid curso ID'}, 400
            professor.curso = curso


        # Save the updated Professor to the database
        db.session.commit()

        return {'message': 'Professor updated successfully'}, 200


    def delete(self, professor_id):
        log.info("Delete - Professores")        
        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()

        if professor is not None:
            professor.excluido_professor = True #para delete físico troca isso aqui por "db.session.delete(professor)"
            db.session.commit()
            return {'message': 'Professor deleted successfully'}, 200

        if not professor:
            return {'message': 'Professor not found'}, 404
    