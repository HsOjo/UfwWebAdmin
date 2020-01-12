from flask import Blueprint, Flask, abort, render_template, url_for

from app import common
from app.base.service import Service
from app.util.log import Log


class Controller:
    import_name = __name__  # type: str
    url_prefix = None  # type: str
    __service__ = None

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

        self.view_funcs = {}

        self.service = None  # type: Service
        if self.__service__ is not None:
            self.service = self.__service__()

    def register_app(self, app: Flask, **options):
        self.app = app
        self.hook_register()
        options.setdefault('url_prefix', self.url_prefix)

        if self.is_development:
            Log.append('-> Register %s on %s' % (self.__class__.__name__, options['url_prefix']))

        self.register_routes()
        app.register_blueprint(self.blueprint, **options)

    def register_route(self, view_func, rule=None, methods=None, **kwargs):
        func_name = view_func.__name__
        if rule is None:
            rule = '/%s' % func_name

        if self.is_development:
            Log.append('\t-> Register %s.%s on %s' % (self.name, func_name, rule))

        controller_view_func = self.view_funcs.get(view_func)
        if controller_view_func is None:
            def controller_view_func(*args, **kwargs):
                try:
                    result = view_func(*args, **kwargs)
                    if self.service is not None:
                        self.service.commit()
                    return result
                except Exception as e:
                    return self.hook_exception(e) or abort(500)

            controller_view_func.__name__ = view_func.__name__
            self.view_funcs[view_func] = controller_view_func

        self.blueprint.add_url_rule(rule, view_func=controller_view_func, methods=methods, **kwargs)

    def hook_exception(self, e: Exception):
        exc = common.get_exception()
        Log.append(self.hook_exception, 'Error', exc)
        if self.is_development:
            return render_template('common/error.html', e=exc), 500

    @property
    def is_development(self):
        return self.app.env == 'development'

    def hook_register(self):
        pass

    def register_routes(self):
        pass

    def url_for(self, endpoint, controller=None, **kwargs):
        controller: Controller
        if controller is None:
            controller = self

        if callable(endpoint):
            endpoint = endpoint.__name__

        return url_for('%s.%s' % (controller.name, endpoint), **kwargs)
