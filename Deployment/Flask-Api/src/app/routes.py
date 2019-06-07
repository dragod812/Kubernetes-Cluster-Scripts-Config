from app import app
from app import api
from app import db
from app import auth
from app.config import Config
from flask_restful import Resource
from flask import request, abort
from functools import wraps


def verifiy_token(view_function) :
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = ""
        if not auth_header :
            abort(401)
        elif len(auth_header.split(" ")) == 1 :
            access_token = auth_header.split(" ")[0]
        else :
            access_token = auth_header.split(" ")[1]
        # TOKEN_QUERY = '''
        # select token from accesstokens where token = ?
        # '''
        # client = db.getClient()
        # result = client.sql(query_str=TOKEN_QUERY, query_args=access_token, include_field_names=False)
        if Config.SECRET_KEY == access_token :
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

class apiVersion(Resource):
    decorators = [verifiy_token]
    def get(self):
        return { 'api-version' : 1.0 }
api.add_resource(apiVersion, '/api')

class SimilarProducts(Resource):
    decorators = [verifiy_token]
    def get(self, product_id):

        SIMILAR_PRODUCTS_QUERY = '''
        select product_attributes.id,product_attributes.name,product_attributes.price,product_attributes.mrp,product_attributes.brand,product_attributes.image,similar_products.simscore from similar_products
        JOIN product_attributes on similar_products.id = product_attributes.id
        where similar_products.id = ?
        '''

        SIMILAR_PRODUCTS_ARGS = [product_id]
        client = db.getClient()
        result = client.sql(query_str=SIMILAR_PRODUCTS_QUERY, query_args=SIMILAR_PRODUCTS_ARGS, include_field_names=True)
        response = {}
        recoList = []
        for i,row in enumerate(result):
            if i == 0 :
                field_names = row
            else :
                newDict = {}
                for j,f in enumerate(field_names) :
                    newDict[f] = row[j]
                recoList.append(newDict)
        response['statusCode'] = 200
        response['pid'] = product_id
        response['algo'] = 'ensemble'
        response['type'] = 'reco'
        response['recommendation'] = recoList
        return response
api.add_resource(SimilarProducts, '/api/recommendations/<string:product_id>')
