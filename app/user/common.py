from flask_login import current_user

from app import login_manager
from .models import UserModel


@login_manager.user_loader
def _load_user(id: int):
    return UserModel.query.get(id)


def get_current_user() -> UserModel:
    return current_user
