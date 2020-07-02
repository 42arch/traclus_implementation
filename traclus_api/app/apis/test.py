from flask import request, Blueprint, jsonify

test = Blueprint('test', __name__)


@test.route('/test/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return 'post test'
    elif request.method == 'GET':
        data = {
            'name': 'flask',
            'lang': 'python'
        }
        return jsonify(data)
