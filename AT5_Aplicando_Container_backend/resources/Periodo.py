from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.periodo import Periodo, periodo_fields

parser = reqparse.RequestParser()
parser.add_argument('semestrereferencia', type=str, help='Problema na conversão do semestre de referência')

class PeriodoResource(Resource):
    @marshal_with(periodo_fields)
    def get(self):
        log.info("Get - Periodos")
        periodos = Periodo.query.filter_by(excluido=False).all()
        return periodos, 200

    def post(self):
        log.info("Post - Periodos")
        args = parser.parse_args()
        semestrereferencia = args['semestrereferencia']

        periodo = Periodo(semestrereferencia=semestrereferencia)
        db.session.add(periodo)
        db.session.commit()

        return {'message': 'Periodo created successfully'}, 201

    
class PeriodosResource(Resource):

    def get(self, periodo_id):
        log.info("Get - Periodos")
        periodo = Periodo.query.filter_by(id=periodo_id, excluido=False).first()

        if (periodo is not None):
            return marshal(periodo, periodo_fields), 201
        else:
            return {'message': 'Periodo not found'}, 404
        
    def put(self, periodo_id):
        log.info("Put - Periodos")
        args = parser.parse_args()

        periodo = Periodo.query.filter_by(id=periodo_id, excluido=False).first()
        if not periodo:
            return {'message': 'Periodo not found'}, 404

        if args['semestrereferencia']:
            periodo.semestrereferencia = args['semestrereferencia']
        db.session.commit()

        return {'message': 'Periodo updated successfully'}, 200

    def delete(self, periodo_id):
        log.info("Delete - Periodos")
        periodo = Periodo.query.filter_by(id=periodo_id, excluido=False).first()

        if periodo is not None:
            periodo.excluido = True #para delete físico troca isso aqui por "db.session.delete(periodo)"
            db.session.commit()
            return {'message': 'Periodo deleted successfully'}, 200

        if not periodo:
            return {'message': 'Periodo not found'}, 404
    