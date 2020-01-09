from app import db
from app.base import Model


class SettingModel(db.Model, Model):
    __tablename__ = 'setting'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    key = db.Column(db.VARCHAR, unique=True)
    value = db.Column(db.VARCHAR)
