from app.apis.algorithm_apis import algorithm
from app.apis.test import test
# from app.apis.user import user


# 路由蓝图注册
def register_blueprint(app):
    app.register_blueprint(test)
    # app.register_blueprint(user, url_prefix='/api')
    app.register_blueprint(algorithm, url_prefix='/api')
