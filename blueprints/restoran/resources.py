from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Restoran
from blueprints.lokasi.model import Lokasi
from blueprints.menu.model import Menu
from blueprints import db, app
from sqlalchemy import desc

from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

bp_Restoran = Blueprint('table_Restoran', __name__)
api = Api(bp_Restoran)


class RestoranResource(Resource):
    def get(self, id):
        qry = Restoran.query.get(id)
        if qry is not None:
            return marshal(qry, Restoran.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('gambar', location='json')
        parser.add_argument('gambar1', location='json')
        parser.add_argument('gambar2', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('promo', location='json', type=bool)
        parser.add_argument('diskon', location='json', type=int)
        parser.add_argument('kota', location='json')
        parser.add_argument('menu_id', location='json')
        parser.add_argument('lokasi_id', location='json')
        parser.add_argument('lat', location='json')
        parser.add_argument('lon', location='json')
        parser.add_argument('program', location='json')
        parser.add_argument('restoran_pilihan', location='json', type=bool)
        args = parser.parse_args()

        result = Restoran(args['nama'], args['gambar'], args['gambar1'],
                          args['gambar2'], args['harga'], args['promo'], args['diskon'],
                          args['menu_id'], args['lokasi_id'], args['lat'], args['lon'], args['program'], args['restoran_pilihan'])

        db.session.add(result)
        db.session.commit()
        app.logger.debug('DEBUG: %s', result)

        return marshal(result, Restoran.response_fields), 200, {'Content-Type': 'application/json'}

    def delete(self, id):
        qry = Restoran.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200

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


class DaftarRestoran(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Restoran.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            restoran_list = (marshal(row, Restoran.response_fields))
            respon_lokasi = Lokasi.query.filter_by(
                id=restoran_list['lokasi_id']).first()
            result_respon_lokasi = marshal(
                respon_lokasi, Lokasi.response_fields)
            restoran_list['lokasi'] = result_respon_lokasi

            restoran_menu = Menu.query.filter_by(
                id=restoran_list['menu_id']).first()
            result_respon_menu = marshal(restoran_menu, Menu.response_fields)
            restoran_list['menu'] = result_respon_menu

            rows.append(restoran_list)

        return rows, 200


class RestoranSearch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("location", location="args")
        parser.add_argument("keyword", location="args")
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        if args['keyword'] is not None and args['location'] is not None:
            restoran = Restoran.query.filter(
                Restoran.nama.like("%"+args['keyword']+"%"))
            lokasi = Lokasi.query.filter(
                Lokasi.lokasi_restoran.like("%"+args['location']+"%")).all()
            locs_resto = []
            for locs in lokasi:
                lokasi_id = locs.id
                lokasi_resto = restoran.filter_by(
                    lokasi_id=lokasi_id)
                locs_resto.append(lokasi_resto)
            rows = []
            print(locs_resto)
            for nesrow in locs_resto:
                for row in nesrow:
                    restoran_list = (marshal(row, Restoran.response_fields))
                    respon_lokasi = Lokasi.query.filter_by(
                        id=restoran_list['lokasi_id']).first()
                    result_respon_lokasi = marshal(
                        respon_lokasi, Lokasi.response_fields)
                    restoran_list['lokasi'] = result_respon_lokasi
                    restoran_menu = Menu.query.filter_by(
                        id=restoran_list['menu_id']).first()
                    result_respon_menu = marshal(
                        restoran_menu, Menu.response_fields)
                    restoran_list['menu'] = result_respon_menu

                    rows.append(restoran_list)
            return rows, 200

        elif args['keyword'] is None and args['location'] is not None:
            lokasi = Lokasi.query.filter(
                Lokasi.lokasi_restoran.like("%"+args['location']+"%")).all()
            locs_resto = []
            for locs in lokasi:
                lokasi_id = locs.id
                lokasi_resto = Restoran.query.filter_by(
                    lokasi_id=lokasi_id)
                locs_resto.append(lokasi_resto)
            rows = []
            print(locs_resto)
            for nesrow in locs_resto:
                for row in nesrow:
                    restoran_list = (marshal(row, Restoran.response_fields))
                    respon_lokasi = Lokasi.query.filter_by(
                        id=restoran_list['lokasi_id']).first()
                    result_respon_lokasi = marshal(
                        respon_lokasi, Lokasi.response_fields)
                    restoran_list['lokasi'] = result_respon_lokasi
                    restoran_menu = Menu.query.filter_by(
                        id=restoran_list['menu_id']).first()
                    result_respon_menu = marshal(
                        restoran_menu, Menu.response_fields)
                    restoran_list['menu'] = result_respon_menu

                    rows.append(restoran_list)
            return rows, 200

        elif args['keyword'] is not None and args['location'] is None:
            restoran = Restoran.query.filter(
                Restoran.nama.like("%"+args['keyword']+"%"))
            rows = []
            print(restoran)
            for row in restoran:
                restoran_list = (marshal(row, Restoran.response_fields))
                respon_lokasi = Lokasi.query.filter_by(
                    id=restoran_list['lokasi_id']).first()
                result_respon_lokasi = marshal(
                    respon_lokasi, Lokasi.response_fields)
                restoran_list['lokasi'] = result_respon_lokasi
                restoran_menu = Menu.query.filter_by(
                    id=restoran_list['menu_id']).first()
                result_respon_menu = marshal(
                    restoran_menu, Menu.response_fields)
                restoran_list['menu'] = result_respon_menu

                rows.append(restoran_list)

            return rows, 200

        # if args['location'] is not None:
        #     restoran = Lokasi.query.filter(
        #         Lokasi.lokasi_restoran.like("%"+args['location'])+"%")

        # if args['keyword'] is not None:
        #     restoran = Restoran.query.filter(
        #         Restoran.nama.like("%"+args['keyword']+"%"))

        # rows = []
        # for row in restoran:
        #     rows.append(marshal(row, Lokasi.response_fields))

        # rows = []
        # for row in restoran.limit(args['rp']).offset(offset).all():
        #     restoran_list = (marshal(row, Restoran.response_fields))
        #     respon_lokasi = Lokasi.query.filter_by(
        #         id=restoran_list['lokasi_id']).first()
        #     result_respon_lokasi = marshal(
        #         respon_lokasi, Lokasi.response_fields)
        #     restoran_list['lokasi'] = result_respon_lokasi
        #     restoran_menu = Menu.query.filter_by(
        #         id=restoran_list['menu_id']).first()
        #     result_respon_menu = marshal(
        #         restoran_menu, Menu.response_fields)
        #     restoran_list['menu'] = result_respon_menu

        #     rows.append(restoran_list)

        # return marshal(restoran, Restoran.response_fields), 200


api.add_resource(DaftarRestoran, '', '/daftar')
api.add_resource(RestoranResource, '', '/<id>')
api.add_resource(RestoranSearch, '', '/search')

# test
