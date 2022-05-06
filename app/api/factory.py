from flask import Flask 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_login import LoginManager
from os import path
from .cutils import init_celery
import config


PROJECT_PATH = path.dirname(path.realpath(__file__)).split("/")[-1]

db_instance = SQLAlchemy()
migrate = Migrate()
ma_instance = Marshmallow()
core = CORS()
socket = SocketIO()
login_manager = LoginManager()


def create_app(app_name=PROJECT_PATH, **kwargs):
    app = Flask(app_name)
    app.config.from_object(config.DevConf)
    db_instance.init_app(app)
    migrate.init_app(app, db_instance)
    core.init_app(app, resources={r"/*": {"origins": "*"}})
    socket.init_app(app,cors_allowed_origins='*', async_mode='threading')
    login_manager.init_app(app)
    if kwargs.get("celery"):
        init_celery(app, kwargs.get("celery"))
    with app.app_context():
        from api.exsiccate import urls
        from api.users import auth 
        app.add_url_rule('/exsiccate/', view_func=urls.ExsiccateRoute.as_view('exsiccate'))
        # app.add_url_rule('/auth/login', view_func=urls.LoginRoute.as_view('login'))
        db_instance.create_all()
        return app