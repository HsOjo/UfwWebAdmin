from typing import List

from flask import render_template

from app.lib import Rule
from app.main.base import UfwController


class RuleController(UfwController):
    import_name = __name__
    url_prefix = '/rule'

    def register_routes(self):
        self.register_route(self.index, '/')
        self.register_route(self.index)

    def index(self):
        status = self.ufw.status()
        status = dict((k.lower().replace(' ', '_'), v) for k, v in status.items())
        rules = status.pop('rules')  # type: List[Rule]
        return render_template('rule/index.html', rules=rules, status=status)
