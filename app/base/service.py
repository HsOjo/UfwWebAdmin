from typing import List

from sqlalchemy.engine import ResultProxy

from app.base.model import BaseModel


class Service:
    __model__ = BaseModel

    def __init__(self):
        self._q = self.__model__.query

    @property
    def all_items(self):
        return self._q.all()  # type: List[BaseModel]

    def get_item(self, id):
        return self._q.get(id)

    def get_items(self, **data):
        result = self._q.filter_by(**data)  # type: ResultProxy
        return result
