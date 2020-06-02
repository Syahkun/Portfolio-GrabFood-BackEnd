from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
# from blueprints.pengguna.model import Pengguna
from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship


class Restoran(db.Model):
    __tablename__ = 'table_restoran'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), nullable=False)
    gambar = db.Column(db.String(255))
    gambar1 = db.Column(db.String(255))
    gambar2 = db.Column(db.String(255))
    harga = db.Column(db.Integer)
    promo = db.Column(db.Boolean, default=False)
    diskon = db.Column(db.Integer, default=0)
    kota = db.Column(db.String(255))
    menu_id = db.Column(
        db.Integer, db.ForeignKey('table_menu.id'))
    lokasi_id = db.Column(
        db.Integer, db.ForeignKey('table_lokasi.id'))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    program = db.Column(db.String(255))
    restoran_pilihan = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id': fields.Integer,
        'nama': fields.String,
        'gambar': fields.String,
        'gambar1': fields.String,
        'gambar2': fields.String,
        "harga": fields.Integer,
        'promo': fields.Boolean,
        'diskon': fields.Integer,
        'kota': fields.String,
        'menu_id': fields.Integer,
        'lokasi_id': fields.Integer,
        'lat': fields.Float,
        'lon': fields.Float,
        'program': fields.String,
        'restoran_pilihan': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, nama, gambar, gambar1, gambar2, harga, promo, diskon, menu_id, lokasi_id, lat, lon, program, restoran_pilihan):
        self.nama = nama
        self.gambar = gambar
        self.gambar1 = gambar1
        self.gambar2 = gambar2
        self.harga = harga
        self.promo = promo
        self.diskon = diskon
        self.menu_id = menu_id
        self.lokasi_id = lokasi_id
        self.lat = lat
        self.lon = lon
        self.program = program
        self.restoran_pilihan = restoran_pilihan

    def __repr__(self):
        return '<Restoran %r>' % self.id
