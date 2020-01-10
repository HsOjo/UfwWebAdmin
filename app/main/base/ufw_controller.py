from app.lib import Ufw
from app.lib.ufw.test import UfwTest
from app.user.base import AdminController


class UfwController(AdminController):
    def __init__(self):
        super().__init__()
        self.ufw = None  # type: Ufw

    def hook_register(self):
        if self.is_development:
            self.ufw = UfwTest()
        else:
            self.ufw = Ufw()
