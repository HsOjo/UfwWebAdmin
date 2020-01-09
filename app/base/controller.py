from flask import Blueprint, Flask


class Controller:
    import_name = __name__
    url_prefix = None  # type: str

    def __init__(self):
        self.app = None  # type: Flask

        self.name = '.'.join(self.import_name.split('.')[1:])
        if self.url_prefix is None:
            self.url_prefix = '/%s' % self.name.replace('.', '/')

        self.blueprint = Blueprint(self.name, self.import_name)

    def register_app(self, app: Flask, **options):
        self.app = app
        self.register_routes()
        options.setdefault('url_prefix', self.url_prefix)
        app.register_blueprint(self.blueprint, **options)

        print('  -> Register %a on %a' % (self, options['url_prefix']))

    def register_route(self, rule, view_func, methods=None, **kwargs):
        self.blueprint.add_url_rule(rule, view_func=view_func, methods=methods, **kwargs)

    def register_routes(self):
        pass