from flask import Flask, request, jsonify
from flask_restx import Api, Resource

from routing.routes import *


def register_api(api):
    api.add_resource(Employees, '/api/employees', '/api/employees/<int:pin>')
    api.add_resource(Articles, '/api/articles', '/api/articles/<string:article_id_ean>')


app = Flask(__name__)
api = Api(app)

register_api(api)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
