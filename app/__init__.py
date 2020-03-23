from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_moment import Moment
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)

    from .server import server
    from .auth import auth
    from .murid import murid

    app.register_blueprint(server)
    app.register_blueprint(murid)
    app.register_blueprint(auth)

    with app.app_context():
        pass

    return app
