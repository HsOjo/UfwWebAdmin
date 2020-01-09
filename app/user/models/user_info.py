from app import db
from app.base import Model
from app.user.models import UserModel


class UserInfoModel(db.Model, Model):
    __tablename__ = 'user_info'

    user: UserModel

    user_id = db.Column(db.INTEGER, db.ForeignKey(UserModel.id), primary_key=True)
    nickname = db.Column(db.VARCHAR)
    comment = db.Column(db.TEXT)
