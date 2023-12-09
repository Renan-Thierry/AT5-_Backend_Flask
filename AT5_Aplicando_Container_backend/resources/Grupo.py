from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers.database import db
from helpers.logger import log
from model.grupo import Grupo, grupo_fields
from model.coordenador import Coordenador
from model.periodo import Periodo


parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, help='Problema na conversão do título')
parser.add_argument('link', type=str, help='Problema na conversão do link')
parser.add_argument('mensagem', type=str, help='Problema na conversão da mensagem')

parser.add_argument('periodo', type=dict, required=True)
parser.add_argument('coordenador', type=dict, required=True)


class GrupoResource(Resource):
    @marshal_with(grupo_fields)
    #@jwt_required()  # Requer autenticação com token para acessar o recurso
    def get(self):
        #identity = get_jwt_identity()
        log.info("Get - Grupos: ")
        grupos = Grupo.query.filter_by(excluido=False).all()
        return grupos, 200
    
    #@jwt_required()  # Requer autenticação com token para acessar o recurso
    def post(self):
        log.info("Post - Grupos")
        args = parser.parse_args()
        titulo = args['titulo']
        link = args['link']
        mensagem = args['mensagem']

        periodo_id = args['periodo']['id']
        coordenador_id = args['coordenador']['id']

        periodo = Periodo.query.filter_by(id=periodo_id, excluido=False).first()
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido=False).first()
        # Create Grupo instance
        if not periodo:
            return {'message': 'Invalid Periodo'}, 400
        if not coordenador:
            return {'message': 'Invalid Coordenador'}, 400
        
        grupo = Grupo(titulo=titulo, link=link, mensagem=mensagem, periodo=periodo, coordenador=coordenador)

        # Save Grupo to the database
        db.session.add(grupo)
        db.session.commit()

        return {'message': 'Group created successfully'}, 201

    
class GruposResource(Resource):
    #@jwt_required()  # Requer autenticação com token para acessar o recurso
    def get(self, grupo_id):
        #identity = get_jwt_identity()
        log.info("Get - Grupos")
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if (grupo is not None):
            return marshal(grupo, grupo_fields), 201
        else:
            return {'message': 'Grupo not found'}, 404
        
    #@jwt_required()  # Requer autenticação com token para acessar o recurso
    def put(self, grupo_id):
        log.info("Put - Grupos")
        args = parser.parse_args()

        # Fetch the Grupo from the database
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if not grupo:
            return {'message': 'Group not found'}, 404

        # Update Grupo attributes based on the request arguments
        grupo.titulo = args.get('titulo', grupo.titulo)
        grupo.link = args.get('link', grupo.link)
        grupo.mensagem = args.get('mensagem', grupo.mensagem)
        periodo_id = args['periodo']['id']
        if periodo_id:
            periodo = Periodo.query.get(periodo_id)
            if not periodo:
                return {'message': 'Invalid Periodo'}, 400
            grupo.periodo = periodo

        coordenador_id = args['coordenador']['id']
        if coordenador_id:
            coordenador = Coordenador.query.get(coordenador_id)
            if not coordenador:
                return {'message': 'Invalid Coordenador'}, 400
            grupo.coordenador = coordenador

        # Save the updated Grupo to the database
        db.session.commit()

        return {'message': 'Group updated successfully'}, 200
    
    #@jwt_required()  # Requer autenticação com token para acessar o recurso
    def delete(self, grupo_id):
        log.info("Delete - Grupos")
        # Fetch the Grupo from the database
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if grupo is not None:
            grupo.excluido = True #para delete físico troca isso aqui por "db.session.delete(grupo)"
            db.session.commit()
            return {'message': 'Grupo deleted successfully'}, 200

        if not grupo:
            return {'message': 'Grupo not found'}, 404
