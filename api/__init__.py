from flask import Flask 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from celery import Celery
import config
import celery_config as cel

db_instance = SQLAlchemy()
migrate = Migrate()
ma_instance = Marshmallow()
core = CORS()
socket = SocketIO()

def make_celery():
    celery = Celery(__name__,broker_url=cel.broker_url, cache_backend=cel.cache_backend, result_backend=cel.result_backend, imports = cel.imports)
    return celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevConf)
    db_instance.init_app(app)
    migrate.init_app(app, db_instance)
    core.init_app(app, resources={r"/*": {"origins": "*"}})
    socket.init_app(app,cors_allowed_origins='*', async_mode='threading')
    with app.app_context():
        from api.exsiccate import urls
        app.add_url_rule('/exsiccate/', view_func=urls.ExsiccateRoute.as_view('exsiccate'))
        app.add_url_rule('/auth/login', view_func=urls.LoginRoute.as_view('login'))
        db_instance.create_all()
        return app

celery = make_celery()