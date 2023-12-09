from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.endereco import Endereco, endereco_fields

parser = reqparse.RequestParser()
parser.add_argument('rua', type=str, help='Problema na conversão da rua')
parser.add_argument('bairro', type=str, help='Problema na conversão do bairro')
parser.add_argument('cep', type=str, help='Problema na conversão do CEP')
parser.add_argument('numero', type=str, help='Problema na conversão do número')
parser.add_argument('complemento', type=str, help='Problema na conversão do complemento')

class EnderecoResource(Resource):
    @marshal_with(endereco_fields)
    def get(self):
        log.info("Get - Endereços")
        enderecos = Endereco.query.filter_by(excluido=False).all()
        return enderecos, 200

    def post(self):
        log.info("Post - Endereços")
        args = parser.parse_args()

        # Extract endereco data from the request arguments
        rua = args['rua']
        bairro = args['bairro']
        cep = args['cep']
        numero = args['numero']
        complemento = args['complemento']

        # Create Endereco instance
        endereco = Endereco(rua=rua, bairro=bairro, cep=cep, numero=numero, complemento=complemento)

        # Save Endereco to the database
        db.session.add(endereco)
        db.session.commit()

        return {'message': 'Endereco created successfully'}, 201

    
class EnderecosResource(Resource):

    def get(self, endereco_id):
        log.info("Get - Endereços")
        endereco = Endereco.query.filter_by(id=endereco_id, excluido=False).first()

        if (endereco is not None):
            return marshal(endereco, endereco_fields), 201
        else:
            return {'message': 'Endereco not found'}, 404
        
    def put(self, endereco_id):
        log.info("Put - Endereços")
        args = parser.parse_args()

        # Fetch the Endereco from the database
        endereco = Endereco.query.filter_by(id=endereco_id, excluido=False).first()

        if not endereco:
            return {'message': 'Endereco not found'}, 404

        # Update Endereco attributes based on the request arguments
        endereco.rua = args.get('rua', endereco.rua)
        endereco.bairro = args.get('bairro', endereco.bairro)
        endereco.cep = args.get('cep', endereco.cep)
        endereco.numero = args.get('numero', endereco.numero)
        endereco.complemento = args.get('complemento', endereco.complemento)

        # Save the updated Endereco to the database
        db.session.commit()

        return {'message': 'Endereco updated successfully'}, 200

    def delete(self, endereco_id):
        log.info("Delete - Endereços")
        # Fetch the Endereco from the database
        endereco = Endereco.query.filter_by(id=endereco_id, excluido=False).first()

        if endereco is not None:
            endereco.excluido = True #para delete físico troca isso aqui por "db.session.delete(endereco)"
            db.session.commit()
            return {'message': 'Endereco deleted successfully'}, 200

        if not endereco:
            return {'message': 'Endereco not found'}, 404
