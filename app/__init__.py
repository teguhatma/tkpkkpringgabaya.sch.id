from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from .server import server

    app.register_blueprint(server)

    with app.app_context():
        pass

    return app
