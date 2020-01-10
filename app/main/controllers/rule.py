from typing import List

from flask import render_template

from app.base import Controller
from app.lib import Ufw, Rule
from app.lib.ufw.test import UfwTest


class RuleController(Controller):
    import_name = __name__

    def __init__(self):
        super().__init__()
        self.ufw = None  # type: Ufw

    def hook_register(self):
        if self.is_development:
            self.ufw = UfwTest()
        else:
            self.ufw = Ufw()

    def register_routes(self):
        self.register_route(self.index, '/')
        self.register_route(self.index)

    def index(self):
        status = self.ufw.status()
        status = dict((k.lower().replace(' ', '_'), v) for k, v in status.items())
        rules = status.pop('rules')  # type: List[Rule]
        return render_template('rule/index.html', rules=rules, status=status)
