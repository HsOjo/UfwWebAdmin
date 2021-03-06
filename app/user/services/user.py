from app.base import Service
from app.user import UserModel


class UserService(Service):
    __model__ = UserModel

    def login(self, username, password):
        items = self.get_items(username=username, password=password)
        item = items.first()  # type: UserModel
        if item is None:
            return False

        return item
