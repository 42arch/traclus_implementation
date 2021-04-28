from flask import Flask

from app.api import register_blueprint
from app.ext import init_ext


def create_app():
    app = Flask(__name__)

    # app.config.from_object()

    init_ext(app)

    register_blueprint(app)

    return app
