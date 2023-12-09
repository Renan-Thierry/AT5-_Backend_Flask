from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.alunogrupo import AlunoGrupo, alunogrupo_fields
from model.aluno import Aluno
from model.grupo import Grupo

parser = reqparse.RequestParser()


parser.add_argument('aluno', type=dict, required=True)
parser.add_argument('grupo', type=dict, required=True)

class AlunoGrupoResource(Resource):
    @marshal_with(alunogrupo_fields)
    def get(self):
        log.info("Get - AlunosGrupo")
        alunosgrupo = AlunoGrupo.query.filter_by(excluido=False).all()
        return alunosgrupo, 200

    def post(self):
        log.info("Post - AlunosGrupo")

        args = parser.parse_args()

        # Fetch the associated objects based on their IDs
        aluno_id = args['aluno']['id']
        grupo_id = args['grupo']['id']

        # Verificar se já existe um aluno com o mesmo aluno_id no grupo
        existing_aluno_grupo = AlunoGrupo.query.filter_by(aluno_id=aluno_id, grupo_id=grupo_id, excluido=False).first()
        if existing_aluno_grupo:
            return {'message': 'Aluno já está associado ao grupo'}, 400

        aluno = Aluno.query.filter_by(id=aluno_id, excluido=False).first()
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if not aluno:
            return {'message': 'Invalid Aluno'}, 400
        if not grupo:
            return {'message': 'Invalid Grupo'}, 400

        # Create Aluno instance
        alunogrupo = AlunoGrupo(aluno=aluno, grupo=grupo)

        # Save Aluno to the database
        db.session.add(alunogrupo)
        db.session.commit()

        return {'message': 'AlunoGrupo created successfully'}, 201
    
class AlunosGrupoResource(Resource):

    def get(self, alunogrupo_id):
        log.info("Get - AlunosGrupo")
        alunogrupo = AlunoGrupo.query.filter_by(id=alunogrupo_id, excluido=False).first()

        if (alunogrupo is not None):
            return marshal(alunogrupo, alunogrupo_fields), 201
        else:
            return {'message': 'AlunoGrupo not found'}, 404

    def put(self, alunogrupo_id):
        log.info("Put - AlunosGrupo")

        args = parser.parse_args()

        # Fetch the Aluno from the database
        alunogrupo = AlunoGrupo.query.filter_by(id=alunogrupo_id, excluido=False).first()

        if not alunogrupo:
            return {'message': 'AlunoGrupo not found'}, 404

        # Update Aluno attributes based on the request args
       

        # Fetch the associated objects based on their IDs if provided
        aluno_id = args['aluno']['id']
        grupo_id = args['grupo']['id']

        if not aluno_id and not grupo_id:
            return {'message': 'Both aluno and grupo IDs are required'}, 400
        
        if aluno_id:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {'message': 'Invalid aluno ID'}, 400
            alunogrupo.aluno = aluno

        if grupo_id:
            grupo = Grupo.query.get(grupo_id)
            if not grupo:
                return {'message': 'Invalid grupo ID'}, 400
            alunogrupo.grupo = grupo

        # Save the updated Aluno to the database
        db.session.commit()

        return {'message': 'AlunoGrupo updated successfully'}, 200

    def delete(self, alunogrupo_id):
        log.info("Delete - Alunos")
        # Fetch the Aluno from the database
        alunogrupo = AlunoGrupo.query.filter_by(id=alunogrupo_id, excluido=False).first()

        if alunogrupo is not None:
            alunogrupo.excluido = True #para delete físico troca isso aqui por "db.session.delete(aluno)"
            db.session.commit()
            return {'message': 'AlunoGrupo deleted successfully'}, 200

        if not alunogrupo:
            return {'message': 'AlunoGrupo not found'}, 404
    