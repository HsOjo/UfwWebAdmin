from flask import Blueprint, Flask, abort


class Controller:
    import_name = __name__  # type: str
    url_prefix = None  # type: str

    def __init__(self):
        self.app = None  # type: Flask

        nodes = self.import_name.split('.')[1:]
        for node in ['controllers']:
            if node in nodes:
                nodes.remove(node)
        self.name = '.'.join(nodes)

        if self.url_prefix is None:
            self.url_prefix = '/%s' % self.name.replace('.', '/')

        self.blueprint = Blueprint(self.name, self.import_name)
        self.endpoints = []

    def register_app(self, app: Flask, **options):
        self.app = app
        options.setdefault('url_prefix', self.url_prefix)

        if self.app.env == 'development':
            print('  -> Register %s on %s' % (self.__class__.__name__, options['url_prefix']))

        self.register_routes()
        app.register_blueprint(self.blueprint, **options)

    def register_route(self, view_func, rule=None, methods=None, **kwargs):
        func_name = view_func.__name__
        if rule is None:
            rule = '/%s' % func_name

        endpoints_str = (self.name + rule.replace('/', '.')).strip('.')
        endpoints = endpoints_str.split('.')

        if self.app.env == 'development':
            print('    -> Register %s on %s' % (endpoints_str, rule))

        def new_view_func(*args, **kwargs):
            try:
                return view_func(*args, **kwargs)
            except Exception as e:
                return self.exception_hook(e) or abort(500)

        new_view_func.__name__ = view_func.__name__
        self.blueprint.add_url_rule(rule, endpoints, view_func=new_view_func, methods=methods, **kwargs)

    def exception_hook(self, e: Exception):
        pass

    def register_routes(self):
        pass
