from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Lokasi
from blueprints.restoran.model import Restoran
from blueprints.menu.model import Menu
from sqlalchemy import desc


bp_lokasi = Blueprint('table_lokasi', __name__)
api = Api(bp_lokasi)


class LokasiResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lokasi_restoran', location='json', required=True)
        parser.add_argument('lat', location='json')
        parser.add_argument('lon', location='json')

        args = parser.parse_args()

        result = Lokasi(args['lokasi_restoran'], args['lat'], args['lon'])
        db.session.add(result)
        db.session.commit()

        app.logger.debug('DEBUG: %s', result)

        return marshal(result, Lokasi.response_fields), 200

    def get(self, id):
        # ambil data dari database
        qry = Lokasi.query.get(id)
        if qry is not None:
            return marshal(qry, Lokasi.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('lokasi_restoran', location='json')
        parser.add_argument('lat', location='json')
        parser.add_argument('lon', location='json')
        args = parser.parse_args()

        qry = Lokasi.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.lokasi_restoran = args['lokasi_restoran']
        qry.lat = args['lat']
        qry.lat = args['lon']
        db.session.commit()

        return marshal(qry, Lokasi.response_fields), 200

    def delete(self, id):
        qry = Lokasi.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class DaftarLokasi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Lokasi.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Lokasi.response_fields))

        return rows, 200

        # parser = reqparse.RequestParser()
        # parser.add_argument('p', type=int, location='args', default=1)
        # parser.add_argument('rp', type=int, location='args', default=25)

        # args = parser.parse_args()
        # offset = (args['p']*args['rp']-args['rp'])
        # qry = Lokasi.query

        # rows = []
        # for row in qry.limit(args['rp']).offset(offset).all():
        #     lokasi_list = marshal(row, Lokasi.response_fields)
        #     respon_restoran = Restoran.query.filter_by(
        #         id=lokasi_list['restoran_id']).first()
        #     # respon_restoran_menu =Menu.query.filter_by(id=respon_restoran.menu_id).first()
        #     result_respon_restoran = marshal(
        #         respon_restoran, Restoran.response_fields)
        #     lokasi_list['restoran'] = result_respon_restoran

        #     lokasi_menu = Menu.query.filter_by(id= lokasi_list['restoran']['menu_id']).first()
        #     result_lokasi_menu = marshal(lokasi_menu, Menu.response_fields)
        #     lokasi_list['restoran']['menu'] = result_lokasi_menu

        #     # respon_restoran_menu =Menu.query.filter_by(id=lokasi_list['menu_id']).first()

        #     rows.append(lokasi_list)

        # return rows, 200


class DaftarLokasiRestoran(Resource):
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('p', type=int, location='args', default=1)
        # parser.add_argument('rp', type=int, location='args', default=25)

        # args = parser.parse_args()
        # offset = (args['p']*args['rp']-args['rp'])
        qry = Lokasi.query

        rows = []
        for row in db.session.query(Lokasi.lokasi_restoran).distinct().all():
            rows.append(row.lokasi_restoran)

        return rows, 200


api.add_resource(DaftarLokasi, '', '/daftar')
api.add_resource(LokasiResource, '', '/<id>')
api.add_resource(DaftarLokasiRestoran, '', '/daftar-lokasi')


#  for row in qry.limit(args['rp']).offset(offset).all():
#             lokasi_list = marshal(row, Lokasi.response_fields)
#             respon_restoran = Restoran.query.filter_by(
#                 id=lokasi_list.restoran_id).first()
#             result_respon_restoran = marshal(
#                 respon_restoran, Restoran.response_fields)
#             lokasi_list['restoran'] = result_respon_restoran
#             rows.append(lokasi_list)
