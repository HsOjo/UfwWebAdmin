from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.database import DatabaseHelper
from app.main import MainController
from app.user import UserController
from config import configs

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
migrate: Migrate

dh = DatabaseHelper(db)


def create_app(env):
    app = Flask(__name__)

    config = configs.get(env)
    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)

    global migrate
    migrate = Migrate(app, db)
    migrate.init_app(app, render_as_batch=True)

    bootstrap.init_app(app)
    bootstrap_cdns = app.extensions['bootstrap']['cdns']
    bootstrap_cdns['bootstrap'] = bootstrap_cdns['local']
    bootstrap_cdns['jquery'] = bootstrap_cdns['local']

    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'
    login_manager.login_message = '请登录后再进行操作'
    login_manager.init_app(app)

    MainController().register_app(app)
    UserController().register_app(app)

    return app
