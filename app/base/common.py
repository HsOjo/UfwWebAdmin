import json


def register_all_callable_object_from_package(app, pkg, is_filter=False):
    for k in dir(pkg):
        f = getattr(pkg, k)
        if callable(f):
            if is_filter:
                app.add_template_filter(f)
            else:
                app.add_template_global(f)


def register_controllers_from_pkg(app, pkg):
    from .controller import Controller
    for name in dir(pkg):
        item = getattr(pkg, name)
        if isinstance(item, type) and issubclass(item, Controller):
            item().register_app(app)


def load_setting(key: str):
    from app.base.services import SettingService
    item = SettingService().get_items(key=key).first()
    if item is not None:
        return json.loads(item.value)
    return None


def save_setting(key: str, value):
    from app.base.services import SettingService
    value = json.dumps(value, ensure_ascii=False)
    SettingService().add_item(key=key, value=value)
