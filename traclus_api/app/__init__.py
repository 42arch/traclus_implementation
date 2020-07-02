from flask import Flask

from app.apis import register_blueprint
from app.ext import init_ext
from config import envs


def create_app(env):
    app = Flask(__name__)

    # 初始化配置
    app.config.from_object(envs.get(env))

    # 初始化第三方插件
    init_ext(app)

    # 注册路由
    register_blueprint(app)

    return app
