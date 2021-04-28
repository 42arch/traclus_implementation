from flask import request, make_response
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage


class FileResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        file_bytes = file.read()
        file_string = file_bytes.decode()
        res = {
            'file_name': file.filename,
            'content': file_string
        }

        return res, 201
