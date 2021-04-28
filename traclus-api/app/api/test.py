from flask import request, Blueprint, jsonify

test = Blueprint('test', __name__)


@test.route('/', methods=['GET'])
def index():
    data = {
        'name': 'traclus-api',
        'msg': 'it works!'
    }
    return jsonify(data)
