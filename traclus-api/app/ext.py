from flask_cors import CORS

cors = CORS()


def init_ext(app):
    cors.init_app(app)
