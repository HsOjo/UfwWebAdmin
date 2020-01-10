from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import Session


class DatabaseHelper:
    def __init__(self, db: SQLAlchemy):
        self._db = db

    def get_all_model_classes(self):
        from app.base.model import Model
        classes = []
        for cls in self._db.Model._decl_class_registry.values():
            if hasattr(cls, '__tablename__') and issubclass(cls, Model):
                classes.append(cls)
        return classes

    @property
    def session(self) -> Session:
        return self._db.session
