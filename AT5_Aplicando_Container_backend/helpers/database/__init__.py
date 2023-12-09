from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#instancia da classe db que é o banco de dados
db = SQLAlchemy()
migrate = Migrate()
