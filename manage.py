from flask.helpers import get_env
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app, register_manage_commands

env = get_env()
app = create_app(env)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
register_manage_commands(manager)

if __name__ == '__main__':
    manager.run()
