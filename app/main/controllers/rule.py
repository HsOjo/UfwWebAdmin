import time

from flask import render_template, redirect, request

from app.main.base import UfwController
from app.main.common import ufw_status, ufw_sync_rule
from app.main.services.rule import RuleService


class RuleController(UfwController):
    import_name = __name__
    url_prefix = '/rule'
    __service__ = RuleService

    def register_routes(self):
        self.register_route(self.index, '/')
        self.register_route(self.index)
        self.register_route(self.delete, '/delete/<int:id>')

    def index(self):
        now = time.time()
        status = ufw_status(self.ufw)
        if now - status.get('rules_time', 0) > 60:
            ufw_sync_rule(self.ufw)

        pagination = self.service.query.paginate()
        return render_template('rule/index.html', pagination=pagination)

    def delete(self, id: int):
        self.service.delete_item(self.service.query.get(id))
        return redirect(request.referrer)
