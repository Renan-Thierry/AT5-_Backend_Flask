from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.pessoa import Pessoa, pessoa_fields
from sqlalchemy.exc import IntegrityError


parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')

class PessoaResource(Resource):
    @marshal_with(pessoa_fields)
    def get(self):
        log.info("Get - Pessoas")
        pessoas = Pessoa.query.filter_by(excluido=False).all()
        return pessoas, 200

    def post(self):
        log.info("Post - Pessoas")
        args = parser.parse_args()

        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']

        try:
            # Check if email or senha already exists
            # Check if email already exists
            if Pessoa.query.filter(Pessoa.email == email).first():
                return {'message': 'Email already exists'}, 400

            # Check if senha already exists
            if Pessoa.query.filter(Pessoa.senha == senha).first():
                return {'message': 'Senha already exists'}, 400

            pessoa = Pessoa(nome, email, senha, telefone)

            db.session.add(pessoa)
            db.session.commit()

            return {'message': 'Person created successfully'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Email or senha already exists'}, 400

        
class PessoasResource(Resource):

    def get(self, pessoa_id):
        log.info("Get - Pessoas")
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if (pessoa is not None):
            return marshal(pessoa, pessoa_fields), 201
        else:
            return {'message': 'Person not found'}, 404

    def put(self, pessoa_id):
        log.info("Put - Pessoas")
        data = request.json

        # Fetch the Coordenador from the database
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if not pessoa:
            return {'message': 'Person not found'}, 404

        # Update person attributes based on the request JSON
        pessoa.nome = data.get('nome', pessoa.nome)
        pessoa.email = data.get('email', pessoa.email)
        pessoa.senha = data.get('senha', pessoa.senha)
        pessoa.telefone = data.get('telefone', pessoa.telefone)
        
        email = data.get('email', pessoa.email)
        senha = data.get('senha', pessoa.senha)

        # Verificar se o email já existe
        if Pessoa.query.filter_by(email=email).filter(Pessoa.id != pessoa_id).first():
            return {'message': 'Email already exists'}, 400

        # Verificar se a senha já existe
        if Pessoa.query.filter_by(senha=senha).filter(Pessoa.id != pessoa_id).first():
            return {'message': 'Senha already exists'}, 400

        # Atualizar os atributos da pessoa
        pessoa.email = email
        pessoa.senha = senha

        
        # Save the updated Coordenador to the database
        db.session.commit()

        return {'message': 'Person updated successfully'}, 200

    def delete(self, pessoa_id):
        log.info("Delete - Pessoas")
        # Fetch the Pessoa from the database
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if pessoa is not None:
            pessoa.excluido = True #para delete físico troca isso aqui por "db.session.delete(pessoa)"
            db.session.commit()
            return {'message': 'Person deleted successfully'}, 200

        if not pessoa:
            return {'message': 'Person not found'}, 404
    

        
