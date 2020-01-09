from flask.helpers import get_env
from flask_script import Manager

from app import create_app

env = get_env()
app = create_app(env)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
