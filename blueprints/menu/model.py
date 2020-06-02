from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class Menu(db.Model):
    __tablename__ = "table_menu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_menu = db.Column(db.String(100), nullable=False, unique=True)
    gambar_menu = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    table_restoran = db.relationship(
        'Restoran', backref="table_menu", lazy=True)

    response_fields = {
        'id': fields.Integer,
        'nama_menu': fields.String,
        'gambar_menu': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, nama_menu, gambar_menu):
        self.nama_menu = nama_menu
        self.gambar_menu = gambar_menu

    def __repr__(self):
        return '<Menu %r>' % self.id
