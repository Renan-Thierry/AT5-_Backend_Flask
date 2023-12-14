from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from helpers.database import db, migrate
import os
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from helpers.utils.MRequisicao import api_bp
from resources.Pessoa import PessoaResource, PessoasResource
from resources.Aluno import AlunoResource, AlunosResource
from resources.Coordenador import CoordenadorResource, CoordenadoresResource
from resources.Curso import CursoResource, CursosResource
from resources.Endereco import EnderecoResource, EnderecosResource
from resources.Grupo import GrupoResource, GruposResource
from resources.Instituicao import InstituicaoResource, InstituicoesResource
from resources.Periodo import PeriodoResource, PeriodosResource
from resources.Professor import ProfessorResource, ProfessoresResource
from resources.Login import UserLogin
from resources.Mensagem import EmailResource
from resources.AlunoGrupo import AlunoGrupoResource, AlunosGrupoResource




app = Flask(__name__)
CORS(app)




# Criado um objeto de configuração com base na variável de ambiente FLASK_ENV
if app.config['ENV'] == 'production':
    app.config.from_object(ProductionConfig())
elif app.config['ENV'] == 'testing':
    app.config.from_object(TestingConfig())
else:
    app.config.from_object(DevelopmentConfig())


db_uri = f"postgresql://{os.getenv('USER_DB', 'postgres')}:{os.getenv('PASSWORD_DB', '123')}@pgsql:{os.getenv('PORT_DB', '5432')}/{os.getenv('DB_NAME', 'models')}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Chave secreta para geração do token
jwt = JWTManager(app)




db.init_app(app)
migrate.init_app(app, db)
api = Api(api_bp, prefix='/api')



api.add_resource(PessoaResource, '/pessoa')
api.add_resource(PessoasResource, '/pessoa/<pessoa_id>')

api.add_resource(AlunoResource, '/aluno')
api.add_resource(AlunosResource, '/aluno/<aluno_id>')

api.add_resource(CoordenadorResource, '/coordenador')
api.add_resource(CoordenadoresResource, '/coordenador/<coordenador_id>')

api.add_resource(CursoResource, '/curso')
api.add_resource(CursosResource, '/curso/<curso_id>')

api.add_resource(EnderecoResource, '/endereco')
api.add_resource(EnderecosResource, '/endereco/<endereco_id>')

api.add_resource(GrupoResource, '/grupo')
api.add_resource(GruposResource, '/grupo/<int:grupo_id>')

api.add_resource(InstituicaoResource, '/instituicao')
api.add_resource(InstituicoesResource, '/instituicao/<int:instituicao_id>')

api.add_resource(PeriodoResource, '/periodo')
api.add_resource(PeriodosResource, '/periodo/<int:periodo_id>')

api.add_resource(ProfessorResource, '/professor')
api.add_resource(ProfessoresResource, '/professor/<int:professor_id>')

api.add_resource(AlunoGrupoResource, '/alunogrupo')
api.add_resource(AlunosGrupoResource, '/alunogrupo/<int:alunogrupo_id>')

api.add_resource(UserLogin, '/login')

app.register_blueprint(api_bp)

api.add_resource(EmailResource, '/send')


if __name__ == '__main__':  
    app.run()
