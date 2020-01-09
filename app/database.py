from flask_sqlalchemy import BaseQuery, Model, SQLAlchemy

from sqlalchemy.orm import Session


class BaseModel(Model):
    query: BaseQuery

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

    def __repr__(self):
        fields = []

        for k, v in self.__dict__.items():

            if k[0] != '_':

                if isinstance(v, BaseModel):
                    fields.append('%s=<%s ...>' % (k, v.__class__.__name__))
                elif isinstance(v, str):
                    fields.append("%s='%s'" % (k, v))
                else:
                    fields.append('%s=%a' % (k, v))

        result = '<%s %s>' % (self.__class__.__name__, ' '.join(fields))
        return result


class DatabaseHelper:
    def __init__(self, db: SQLAlchemy):
        self._db = db

    def get_all_model_classes(self):
        classes = []
        for cls in self._db.Model._decl_class_registry.values():
            if hasattr(cls, '__tablename__') and issubclass(cls, BaseModel):
                classes.append(cls)
        return classes

    @property
    def session(self) -> Session:
        return self._db.session
