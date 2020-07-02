import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')


def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)


class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'INGNEHASDSGFDFGDFHER345MHI5'

    # session 设置
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_SECURE = True
    SESSION_USE_SIGNER = True


# 开发环境（MySQL为例）
class DevelopConfig(Config):
    DEBUG = True
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123",
        "HOST": "localhost",
        "PORT": '3306',
        "NAME": "flaskapidb"
    }
    # 邮件配置
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 25
    MAIL_USERNAME = "xxx@163.com"
    MAIL_PASSWORD = "password"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    MAIL_SUBJECT_PREFIX = '[Flask_API]'

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


# 测试环境(以postgresql为例)
class TestingConfig(Config):
    TESTING = True
    dbinfo = {
        "ENGINE": "postgresql",
        "DRIVER": "psycopg2",
        "USER": "postgres",
        "PASSWORD": "123",
        "HOST": "localhost",
        "PORT": '5432',
        "NAME": "testdb"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


# 部署环境
class StagingConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123!",
        "HOST": "localhost",
        "PORT": '3306',
        "NAME": "FlaskStagingDb"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


# 生产环境
class ProductConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "Home410793!",
        "HOST": "localhost",
        "PORT": '3306',
        "NAME": "FlaskProductDb"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}

