from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.controleAluno import ControleAluno, controleAlunos_fields

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão da nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('matricula', type=str, help='Problema na conversão do matricula')
parser.add_argument('numero', type=str, help='Problema na conversão do número')
parser.add_argument('curso', type=str, help='Problema na conversão do curso')

class ControleAlunoResource(Resource):
    @marshal_with(controleAlunos_fields)
    def get(self):
        log.info("Get - ControleAlunos")
        controleAlunos = ControleAluno.query.filter_by(excluido=False).all()
        return controleAlunos, 200

    def post(self):
        log.info("Post - ControleAlunos")
        args = parser.parse_args()

        # Extract ControleAluno data from the request arguments
        nome = args['nome']
        email = args['email']
        numero = args['numero']
        matricula = args['matricula']
        curso = args['curso']

        # Create ControleAluno instance
        controleDeAlunos = ControleAluno(nome=nome, email=email, numero=numero, matricula=matricula, curso=curso)

        # Save ControleAluno to the database
        db.session.add(controleDeAlunos)
        db.session.commit()

        return {'message': 'ControleAluno created successfully'}, 201

    
class controleAlunosResource(Resource):

    def get(self, ControleAluno_id):
        log.info("Get - ControleAluno")
        controleDeAlunos = ControleAluno.query.filter_by(id=ControleAluno_id, excluido=False).first()

        if (controleDeAlunos is not None):
            return marshal(controleDeAlunos, controleAlunos_fields), 201
        else:
            return {'message': 'ControleAluno not found'}, 404
        
    def put(self, ControleAluno_id):
        log.info("Put - Endereços")
        args = parser.parse_args()

        # Fetch the ControleAluno from the database
        controleDeAlunos = ControleAluno.query.filter_by(id=ControleAluno_id, excluido=False).first()

        if not controleDeAlunos:
            return {'message': 'ControleAluno not found'}, 404

        # Update ControleAluno attributes based on the request arguments
        controleDeAlunos.nome = args.get('nome', controleDeAlunos.nome)
        controleDeAlunos.email = args.get('email', controleDeAlunos.email)
        controleDeAlunos.matricula = args.get('matricula', controleDeAlunos.matricula)
        controleDeAlunos.numero = args.get('numero', controleDeAlunos.numero)
        controleDeAlunos.curso = args.get('curso', controleDeAlunos.curso)

        # Save the updated ControleAluno to the database
        db.session.commit()

        return {'message': 'ControleAluno updated successfully'}, 200

    def delete(self, ControleAluno_id):
        log.info("Delete - Endereços")
        # Fetch the ControleAluno from the database
        ControleAluno = ControleAluno.query.filter_by(id=ControleAluno_id, excluido=False).first()

        if ControleAluno is not None:
            ControleAluno.excluido = True #para delete físico troca isso aqui por "db.session.delete(ControleAluno)"
            db.session.commit()
            return {'message': 'ControleAluno deleted successfully'}, 200

        if not ControleAluno:
            return {'message': 'ControleAluno not found'}, 404
