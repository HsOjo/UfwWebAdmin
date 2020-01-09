from flask import render_template
from flask_login import login_required

from app.base import Controller


class InfoController(Controller):
    import_name = __name__
    url_prefix = '/user'

    def register_routes(self):
        self.register_route(self.info, '/')

    def exception_hook(self, e: Exception):
        print(e)
        if self.app.env == 'development':
            return render_template('common/error.html', e=e), 500

    @login_required
    def info(self):
        return 'test'
