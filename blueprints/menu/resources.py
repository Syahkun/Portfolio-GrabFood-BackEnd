from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Menu
from sqlalchemy import desc


bp_menu = Blueprint('table_menu', __name__)
api = Api(bp_menu)


class MenuResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_menu', location='json', required=True)
        parser.add_argument('gambar_menu', location='json', required=True)

        args = parser.parse_args()

        result = Menu(args['nama_menu'], args['gambar_menu'])
        db.session.add(result)
        db.session.commit()

        app.logger.debug('DEBUG: %s', result)

        return marshal(result, Menu.response_fields), 200

    def get(self, id):
        # ambil data dari database
        qry = Menu.query.get(id)
        if qry is not None:
            return marshal(qry, Menu.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_menu', location='json')
        parser.add_argument('gambar_menu', location='json')
        args = parser.parse_args()

        qry = Menu.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.nama_menu = args['nama_menu']
        qry.gambar_menu = args['gambar_menu']
        db.session.commit()

        return marshal(qry, Menu.response_fields), 200

    def delete(self, id):
        qry = Menu.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class DaftarMenu(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Menu.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Menu.response_fields))

        return rows, 200


api.add_resource(DaftarMenu, '', '/daftar')
api.add_resource(MenuResource, '', '/<id>')
