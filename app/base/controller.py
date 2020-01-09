from flask import Blueprint, Flask, abort


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
        options.setdefault('url_prefix', self.url_prefix)
        print('  -> Register %a on %a' % (self, options['url_prefix']))
        self.register_routes()
        app.register_blueprint(self.blueprint, **options)

    def register_route(self, view_func, rule=None, methods=None, **kwargs):
        if rule is None:
            rule = '/%s' % view_func.__name__

        print('    -> Register %a on %a' % (view_func, rule))

        def new_view_func(*args, **kwargs):
            try:
                return view_func(*args, **kwargs)
            except Exception as e:
                return self.exception_hook(e) or abort(500)

        new_view_func.__name__ = view_func.__name__
        self.blueprint.add_url_rule(rule, view_func=new_view_func, methods=methods, **kwargs)

    def exception_hook(self, e: Exception):
        pass

    def register_routes(self):
        pass
