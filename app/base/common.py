from .controller import Controller


def register_controllers_from_pkg(app, pkg):
    for name in dir(pkg):
        item = getattr(pkg, name)
        if isinstance(item, type) and issubclass(item, Controller):
            item().register_app(app)
