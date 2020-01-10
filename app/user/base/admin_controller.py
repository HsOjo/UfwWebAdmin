from app.base import Controller
from app.user import admin_required


class AdminController(Controller):
    def __init__(self):
        super().__init__()
        self.admin_views = {}

    def register_route(self, view_func, rule=None, methods=None, **kwargs):
        admin_func = self.admin_views.get(view_func)
        if admin_func is None:
            admin_func = admin_required(view_func)
            self.admin_views[view_func] = admin_func
        super().register_route(admin_func, rule, methods, **kwargs)
