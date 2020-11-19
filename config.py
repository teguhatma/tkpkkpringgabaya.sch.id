import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ADMIN_TK = os.environ.get("ADMIN_TK")
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgres://vqosmtpcivspjf:164b513ca8b7320784edb19331b0bb029600a44b1c844752af1813ea57add65a@ec2-3-218-75-21.compute-1.amazonaws.com:5432/dco0ag7si7knja"
        or "sqlite:///" + os.path.join(basedir, "app.db")
    )
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
