from flask_restful import fields
from helpers.database import db

periodo_fields = {
    'id': fields.Integer,
    'semestrereferencia': fields.String
}

class Periodo(db.Model):
    __tablename__ = "periodo"

    id = db.Column(db.Integer, primary_key=True)
    semestrereferencia = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico

    

    def __init__(self, semestrereferencia):
        self.semestrereferencia = semestrereferencia
        self.excluido = False

    def __repr__(self):
        return f'<Periodo {self.semestrereferencia}>'
