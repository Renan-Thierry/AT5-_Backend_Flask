from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.instituicao import Instituicao, instituicao_fields
from model.endereco import Endereco

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('endereco', type=dict, required=True)

class InstituicaoResource(Resource):
    @marshal_with(instituicao_fields)
    def get(self):
        log.info("Get - Instituições")
        instituicoes = Instituicao.query.filter_by(excluido=False).all()
        return instituicoes, 200

    def post(self):
        log.info("Post - Instituições")
        args = parser.parse_args()
        nome = args['nome']

        endereco_id = args['endereco']['id']

        # Fetch Instituicao and Curso from the database
        endereco = Endereco.query.filter_by(id=endereco_id, excluido=False).first()

        if not endereco:
            return {'message': 'Invalid Endereco'}, 400

        instituicao = Instituicao(nome=nome, endereco=endereco)
        db.session.add(instituicao)
        db.session.commit()

        return {'message': 'Instituicao created successfully'}, 201

    
class InstituicoesResource(Resource):

    def get(self, instituicao_id):
        log.info("Get - Instituições")
        instituicao = Instituicao.query.filter_by(id=instituicao_id, excluido=False).first()

        if (instituicao is not None):
            return marshal(instituicao, instituicao_fields), 201
        else:
            return {'message': 'Instituicao not found'}, 404
        
    def put(self, instituicao_id):
        log.info("Put - Instituições")
        args = parser.parse_args()

        instituicao = Instituicao.query.filter_by(id=instituicao_id, excluido=False).first()
        if not instituicao:
            return {'message': 'Instituicao not found'}, 404

        if args['nome']:
            instituicao.nome = args['nome']

        endereco_id = args['endereco']['id']
        if endereco_id:
            endereco = Endereco.query.get(endereco_id)
            if not endereco:
                return {'message': 'Invalid Endereco'}, 400
            instituicao.endereco = endereco

        db.session.commit()

        return {'message': 'Instituicao updated successfully'}, 200

    def delete(self, instituicao_id):
        log.info("Delete - Instituições")
        instituicao = Instituicao.query.filter_by(id=instituicao_id, excluido=False).first()

        if instituicao is not None:
            instituicao.excluido = True #para delete físico troca isso aqui por "db.session.delete(instituicao)"
            db.session.commit()
            return {'message': 'Instituicao deleted successfully'}, 200

        if not instituicao:
            return {'message': 'Instituicao not found'}, 404
    