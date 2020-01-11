from flask import render_template

from app.main.base import UfwController
from app.main.common import ufw_status


class IndexController(UfwController):
    import_name = __name__
    url_prefix = '/'

    def register_routes(self):
        self.register_route(self.index, '/')
        self.register_route(self.index)

    def index(self):
        status = ufw_status(self.ufw, 3)
        default = status.pop('default', None)
        return render_template('main/index.html', status=status, default=default)
