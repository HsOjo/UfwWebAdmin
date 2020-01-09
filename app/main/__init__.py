from app.base.controller import Controller


class MainController(Controller):
    import_name = __name__
    url_prefix = '/'

    def register_routes(self):
        self.register_route(self.test)

    def test(self):
        return 'test'
