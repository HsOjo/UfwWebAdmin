from flask import render_template
from flask_login import login_required

from app.main.base import UfwController


class IndexController(UfwController):
    import_name = __name__
    url_prefix = '/'

    def register_routes(self):
        self.register_route(self.index)
        self.register_route(self.index, '/')

    @login_required
    def index(self):
        status = self.ufw.status(parse_rule=False)
        default = status.pop('Default', None)

        return render_template('main/index.html', status=status, default=default)
