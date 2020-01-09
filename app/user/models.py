from flask_login import UserMixin

from app import db
from app.base.model import BaseModel


class UserModel(UserMixin, db.Model, BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR, unique=True)
    password = db.Column(db.VARCHAR)
    is_admin = db.Column(db.BOOLEAN, default=False, nullable=False)

    info = db.relationship('UserInfoModel', backref='user', uselist=False, cascade='all')


class UserInfoModel(db.Model, BaseModel):
    __tablename__ = 'user_info'

    user: UserModel

    user_id = db.Column(db.INTEGER, db.ForeignKey(UserModel.id), primary_key=True)
    nickname = db.Column(db.VARCHAR)
    comment = db.Column(db.TEXT)
