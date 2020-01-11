import time

from flask import render_template

from app.main.base import UfwController
from app.main.common import ufw_status, ufw_sync_rule
from app.main.services.rule import RuleService


class RuleController(UfwController):
    import_name = __name__
    url_prefix = '/rule'

    def register_routes(self):
        self.register_route(self.index, '/')
        self.register_route(self.index)

    def index(self):
        now = time.time()
        status = ufw_status(self.ufw)
        if now - status.get('rules_time', 0) > 60:
            ufw_sync_rule(self.ufw)

        service = RuleService()
        pagination = service.query.paginate()
        return render_template('rule/index.html', pagination=pagination)
