from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.curso import Curso, curso_fields
from model.instituicao import Instituicao

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('instituicao', type=dict)

class CursoResource(Resource):
    @marshal_with(curso_fields)
    def get(self):
        log.info("Get - Cursos")
        cursos = Curso.query.filter_by(excluido=False).all()
        return cursos, 200

    def post(self):
        log.info("Post - Cursos")
        args = parser.parse_args()
        nome = args['nome']
        instituicao_data = args['instituicao']
        instituicao_id = instituicao_data['id']

        # Fetch Instituicao from the database
        instituicao = Instituicao.query.filter_by(id=instituicao_id, excluido=False).first()

        if not instituicao:
            return {'message': 'Invalid Instituicao'}, 400

        # Create Curso instance
        curso = Curso(nome=nome, instituicao=instituicao)

        # Save Curso to the database
        db.session.add(curso)
        db.session.commit()

        return {'message': 'Curso created successfully'}, 201

    
class CursosResource(Resource):

    def get(self, curso_id):
        log.info("Get - Cursos")
        curso = Curso.query.filter_by(id=curso_id, excluido=False).first()

        if (curso is not None):
            return marshal(curso, curso_fields), 201
        else:
            return {'message': 'Curso not found'}, 404
        
    def put(self, curso_id):
        log.info("Put - Cursos")
        args = parser.parse_args()

        # Fetch the Curso from the database
        curso = Curso.query.filter_by(id=curso_id, excluido=False).first()

        if not curso:
            return {'message': 'Curso not found'}, 404

        # Update Curso attributes based on the request arguments
        curso.nome = args.get('nome', curso.nome)

        instituicao_data = args.get('instituicao')
        if instituicao_data:
            if 'id' in instituicao_data:
                instituicao_id = instituicao_data['id']
                instituicao = Instituicao.query.get(instituicao_id)
                if not instituicao:
                    return {'message': 'Invalid Instituicao'}, 400
            else:
                return {'message': 'Invalid Instituicao'}, 400

            curso.instituicao = instituicao


        # Save the updated Curso to the database
        db.session.commit()

        return {'message': 'Curso updated successfully'}, 200

    def delete(self, curso_id):
        log.info("Delete - Cursos")
        # Fetch the Curso from the database
        curso = Curso.query.filter_by(id=curso_id, excluido=False).first()

        if curso is not None:
            curso.excluido = True #para delete físico troca isso aqui por "db.session.delete(curso)"
            db.session.commit()
            return {'message': 'Curso deleted successfully'}, 200

        if not curso:
            return {'message': 'Curso not found'}, 404
