from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import common
from app.commands import register_manage_commands
from app.database import DatabaseHelper
from app.errors import register_app_errors
from app.res.language.english import English
from app.util.log import Log
from config import configs

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
migrate: Migrate
language: English

dh = DatabaseHelper(db)


def register_all_callable_object_from_package(app, pkg, is_filter=False):
    for k in dir(pkg):
        f = getattr(pkg, k)
        if callable(f):
            if is_filter:
                app.add_template_filter(f)
            else:
                app.add_template_global(f)


def create_app(env):
    Log.init_app(True, env == 'development')
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

    from app import main, user
    from app.base.common import register_controllers_from_pkg
    register_controllers_from_pkg(app, main)
    register_controllers_from_pkg(app, user)

    register_app_errors(app)

    return app
