from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class Pengguna(db.Model):
    __tablename__ = "table_pengguna"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_pengguna = db.Column(db.String(100), nullable=False, unique=True)
    kata_kunci = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    makanan_favorit = db.Column(db.String(2000))
    alamat = db.Column(db.String(255))
    kota_pengguna = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id': fields.Integer,
        'nama_pengguna': fields.String,
        'kata_kunci': fields.String,
        'makanan_favorit': fields.String,
        'alamat': fields.String,
        'kota_pengguna': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    # disimpan di jwt nya dulu
    jwt_claims_fields = {
        'id': fields.Integer,
        'nama_pengguna': fields.String,
    }

    def __init__(self, nama_pengguna, kata_kunci,  makanan_favorit,  alamat, kota_pengguna, salt):
        self.nama_pengguna = nama_pengguna
        self.kata_kunci = kata_kunci
        self.makanan_favorit = makanan_favorit
        self.alamat = alamat
        self.kota_pengguna = kota_pengguna
        self.salt = salt

    def __repr__(self):
        return '<Pengguna %r>' % self.id
