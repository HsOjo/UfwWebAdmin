from app.base.controller import Controller


class UserController(Controller):
    import_name = __name__

    def register_routes(self):
        self.register_route('/login', self.login, methods=['GET', 'POST'])

    def login(self):
        return 'login'