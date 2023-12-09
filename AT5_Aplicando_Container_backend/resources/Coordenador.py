from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.coordenador import Coordenador, coordenador_fields
from model.curso import Curso
from sqlalchemy.exc import IntegrityError
from model.pessoa import Pessoa



parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('disciplina', type=str, help='Problema na conversão da disciplina')
parser.add_argument('registrodeTrabalho', type=str, help='Problema na conversão do registro de trabalho')

parser.add_argument('curso', type=dict, required=True)


class CoordenadorResource(Resource):
    @marshal_with(coordenador_fields)
    def get(self):
        log.info("Get - Coordenadores")
        coordenadores = Coordenador.query.filter_by(excluido_coordenador=False).all()
        return coordenadores, 200

    def post(self):
        log.info("Post - Coordenadores")

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        disciplina = args['disciplina']
        registrodeTrabalho = args['registrodeTrabalho']

        # Extract Curso data from the request JSON
        curso_coordenador_id = args['curso']['id']

        # Fetch Instituicao and Curso from the database
        curso = Curso.query.filter_by(id=curso_coordenador_id, excluido=False).first()

        if not curso:
            return {'message': 'Invalid Curso'}, 400
        
        try:
            # Check if email or senha already exists
            # Check if email already exists
            if Pessoa.query.filter(Coordenador.email == email).first():
                return {'message': 'Email already exists'}, 400

            # Check if senha already exists
            if Pessoa.query.filter(Coordenador.senha == senha).first():
                return {'message': 'Senha already exists'}, 400

            # Create Coordenador instance
            coordenador = Coordenador(nome=nome, email=email, senha=senha, telefone=telefone,
                                    disciplina=disciplina, registrodeTrabalho=registrodeTrabalho, curso=curso)

            # Save Coordenador to the database
            coordenador.curso_coordenador_id = curso.id
            db.session.add(coordenador)
            db.session.commit()

            return {'message': 'Coordenador created successfully'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Email or senha already exists'}, 400

    
class CoordenadoresResource(Resource):

    def get(self, coordenador_id):
        log.info("Get - Coordenadores")
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido_coordenador=False).first()

        if (coordenador is not None):
            return marshal(coordenador, coordenador_fields), 201
        else:
            return {'message': 'Coordenador not found'}, 404
        
    def put(self, coordenador_id):
        log.info("Put - Coordenadores")
        data = request.json

        # Fetch the Coordenador from the database
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido_coordenador=False).first()

        if not coordenador:
            return {'message': 'Coordenador not found'}, 404

        # Update Coordenador attributes based on the request JSON
        coordenador.nome = data.get('nome', coordenador.nome)
        coordenador.email = data.get('email', coordenador.email)
        coordenador.senha = data.get('senha', coordenador.senha)
        coordenador.telefone = data.get('telefone', coordenador.telefone)
        coordenador.disciplina = data.get('disciplina', coordenador.disciplina)
        coordenador.registrodeTrabalho = data.get('registrodeTrabalho', coordenador.registrodeTrabalho)

        # Fetch the associated Curso object if provided
        curso_coordenador_id = data['curso'].get('id')
        if curso_coordenador_id:
            curso = Curso.query.get(curso_coordenador_id)
            if not curso:
                return {'message': 'Invalid curso ID'}, 400
            coordenador.curso = curso

        try:
            # Check if email already exists for another Coordenador
            if Coordenador.query.filter((Coordenador.email == coordenador.email) & (Coordenador.id != coordenador_id)).first():
                return {'message': 'Email already exists'}, 400

            # Check if senha already exists for another Coordenador
            if Coordenador.query.filter((Coordenador.senha == coordenador.senha) & (Coordenador.id != coordenador_id)).first():
                return {'message': 'Senha already exists'}, 400
            
            if Coordenador.query.filter((Coordenador.nome == coordenador.nome) & (Coordenador.id != coordenador_id)).first():
                return {'message': 'Nome Ja Existente!'}, 400

            # Save the updated Coordenador to the database
            db.session.commit()

            return {'message': 'Coordenador updated successfully'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Email or senha already exists'}, 400


    def delete(self, coordenador_id):
        log.info("Delete - Coordenadores")
        # Fetch the Coordenador from the database
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido_coordenador=False).first()

        if coordenador is not None:
            coordenador.excluido_coordenador = True #para delete físico troca isso aqui por "db.session.delete(coordenador)"
            db.session.commit()
            return {'message': 'Coordenador deleted successfully'}, 200

        if not coordenador:
            return {'message': 'Coordenador not found'}, 404
