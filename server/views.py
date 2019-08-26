from flask_restful import Resource, reqparse
from flask_login import login_required
from flask import jsonify

parser = reqparse.RequestParser()

class SecretResource(Resource):
    @login_required
    def get(self):
        return jsonify({
            'answer': 42
        })