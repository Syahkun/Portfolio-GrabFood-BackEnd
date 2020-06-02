from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class Lokasi(db.Model):
    __tablename__ = "table_lokasi"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lokasi_restoran = db.Column(db.String(2000), unique=True, nullable=False)
    table_restoran = db.relationship(
        'Restoran', backref="table_lokasi", lazy=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id': fields.Integer,
        'lokasi_restoran': fields.String,
        'lat': fields.Float,
        'lon': fields.Float,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, lokasi_restoran, lat, lon):
        self.lokasi_restoran = lokasi_restoran
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<Lokasi %r>' % self.id
