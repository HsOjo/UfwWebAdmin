from functools import wraps
from os import abort

from flask_login import current_user, login_required

from app import login_manager
from app.user.models import UserModel


@login_manager.user_loader
def _load_user(id: int):
    return UserModel.query.get(id)


def get_current_user() -> UserModel:
    return current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not get_current_user().is_admin:
            return abort(403)
        return func(*args, **kwargs)

    return login_required(decorated_view)
