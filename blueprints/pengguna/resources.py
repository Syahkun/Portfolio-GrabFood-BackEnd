from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from blueprints.pengguna.model import Pengguna
from sqlalchemy import desc
import uuid
import hashlib

bp_pengguna = Blueprint('table_pengguna', __name__)
api = Api(bp_pengguna)


class PenggunaResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='json', required=True)
        parser.add_argument('kata_kunci', location='json')
        parser.add_argument('makanan_favorit', location='json')
        parser.add_argument('alamat', location='json')
        parser.add_argument('kota_pengguna', location='json')

        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['kata_kunci'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        result = Pengguna(args['nama_pengguna'], hash_pass,
                          args['makanan_favorit'], args['alamat'], args['kota_pengguna'], salt)
        db.session.add(result)
        db.session.commit()

        app.logger.debug(('DEBUG: %s', result))

        return marshal(result, Pengguna.response_fields), 200

    def get(self, id):
        qry = Pengguna.query.get(id)
        if qry is not None:
            return marshal(qry, Pengguna.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'belum daftar broo, daftar dulu...'}, 404, {'Content-Type': 'application/json'}

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='json', required=True)
        parser.add_argument('kata_kunci', location='json')
        parser.add_argument('makanan_favorit', location='json')
        parser.add_argument('alamat', location='json')
        parser.add_argument('kota_pengguna', location='json')

        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['kata_kunci'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        qry = Pengguna.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.nama_pengguna = args['nama_pengguna']
        qry.kata_kunci = hash_pass
        qry.makanan_favorit = args['makanan_favorit']
        qry.alamat = args['alamat']
        qry.kota_pengguna = args['kota_pengguna']
        qry.salt = salt
        db.session.commit()

        return marshal(qry, Pengguna.response_fields), 200

    def delete(self, id):
        qry = Pengguna.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class DaftarPengguna(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Pengguna.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Pengguna.response_fields))

        return rows, 200


api.add_resource(DaftarPengguna, '', '/daftar')
api.add_resource(PenggunaResource, '', '/<id>')
