from flask_login import login_required

from app.base import Controller


class InfoController(Controller):
    import_name = __name__
    url_prefix = '/user'

    def register_routes(self):
        self.register_route(self.index, '/')

    @login_required
    def index(self):
        return 'test'
