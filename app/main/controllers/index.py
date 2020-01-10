from flask import render_template
from flask_login import login_required

from app.base import Controller


class IndexController(Controller):
    import_name = __name__
    url_prefix = '/'

    def register_routes(self):
        self.register_route(self.index)
        self.register_route(self.index, '/')

    @login_required
    def index(self):
        return render_template('main/index.html')
