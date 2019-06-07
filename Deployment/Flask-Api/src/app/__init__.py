from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


from app.db_support import Database 
db = Database()
from app import routes





