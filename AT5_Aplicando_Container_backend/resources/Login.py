from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from model.coordenador import Coordenador


class UserLogin(Resource):
    def post(self):
       
        data = request.get_json()
        email = data['email']
        senha = data['senha']

        # Verificar credenciais do usuário no banco de dados
        coordenador = Coordenador.query.filter_by(email=email, senha=senha).first()

        if coordenador:
            # Gerar e retornar o token de autenticação
            access_token = create_access_token(identity=email)
            return {'access_token': access_token}, 200
        else:
            return {'error': 'Credenciais inválidas.'}, 401

        