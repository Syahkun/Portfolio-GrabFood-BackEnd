from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

import hashlib
import uuid

from ..pengguna.model import Pengguna

bp_login = Blueprint('login', __name__)
api = Api(bp_login)

class CreateTokenResource(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='args', required=True)
        parser.add_argument('kata_kunci', location='args', required=True)
        args = parser.parse_args()
        
        qry_pengguna = Pengguna.query.filter_by(nama_pengguna=args['nama_pengguna']).first()
        
        if qry_pengguna is not None:
            pengguna_salt = qry_pengguna.salt
            encoded = ('%s%s' %
                       (args['kata_kunci'], pengguna_salt)).encode('utf-8')
            hash_pass =  hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_pengguna.kata_kunci and qry_pengguna.nama_pengguna == args['nama_pengguna']:
                qry_pengguna = marshal(qry_pengguna, Pengguna.jwt_claims_fields)
                qry_pengguna['identifier'] = "thrkobar"
                token = create_access_token(
                    identity=args['nama_pengguna'], user_claims=qry_pengguna)
                return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 404

api.add_resource(CreateTokenResource, '')