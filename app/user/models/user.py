from flask_login import UserMixin

from app import db
from app.base import Model


class UserModel(UserMixin, db.Model, Model):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR, unique=True)
    password = db.Column(db.VARCHAR)
    is_admin = db.Column(db.BOOLEAN, default=False, nullable=False)

    info = db.relationship('UserInfoModel', backref='user', uselist=False, cascade='all')
