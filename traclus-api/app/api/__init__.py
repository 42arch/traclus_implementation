from app.api.algorithm_api import traclus
from app.api.test import test


def register_blueprint(app):
    app.register_blueprint(test)
    app.register_blueprint(traclus, url_prefix='/api')
