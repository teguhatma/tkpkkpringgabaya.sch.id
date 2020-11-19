from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_login import LoginManager
from flask_share import Share

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
share = Share()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    share.init_app(app)
    login_manager.init_app(app)

    from .server import server
    from .auth import auth
    from .murid import murid
    from .client import client

    app.register_blueprint(server)
    app.register_blueprint(murid)
    app.register_blueprint(client)
    app.register_blueprint(auth)

    if not app.debug and not app.testing:
        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/microblog.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Microblog startup")

    with app.app_context():
        pass

    return app
