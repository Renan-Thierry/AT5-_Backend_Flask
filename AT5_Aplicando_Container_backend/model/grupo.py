from flask_restful import fields
from helpers.database import db
from model.coordenador import Coordenador, coordenador_fields
from model.periodo import Periodo, periodo_fields




grupo_fields = {
    'id': fields.Integer,
    'titulo': fields.String,
    'link': fields.String,
    'mensagem': fields.String,
    'periodo': fields.Nested(periodo_fields),
    'coordenador': fields.Nested(coordenador_fields)

}


class Grupo(db.Model):
    __tablename__ = "grupo"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    mensagem = db.Column(db.String, nullable=False)
    excluido = db.Column(db.Boolean, default=False)


    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'), nullable=False)
    periodo = db.relationship('Periodo', backref='grupos')

    coordenador_id = db.Column(db.Integer, db.ForeignKey('coordenador.id'), nullable=False)
    coordenador = db.relationship('Coordenador', backref='grupos')


    def __init__(self, titulo, link, mensagem, periodo, coordenador):
        self.titulo = titulo
        self.link = link
        self.mensagem = mensagem
        self.periodo = periodo
        self.coordenador = coordenador
        self.excluido = False

    def __repr__(self):
        return f'<Grupo {self.titulo}>'
