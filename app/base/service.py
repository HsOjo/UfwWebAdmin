from sqlalchemy.engine import ResultProxy

from app.base.model import Model


class Service:
    __model__ = Model

    def __init__(self):
        self._queue_add = []
        self._queue_delete = []

    @property
    def query(self):
        return self.__model__.query

    def get_items(self, **data):
        result = self.query.filter_by(**data)  # type: ResultProxy
        return result

    def add_item(self, commit_now=True, **data):
        item = self.__model__(**data)

        self._queue_add.append(item)
        if commit_now:
            self.commit(delete=False)

        return item

    def edit_item(self, item, commit_now=True, **data):
        item = self._check_item(item)

        for k, v in data.items():
            if hasattr(item, k):
                setattr(item, k, v)

        self._queue_add.append(item)
        if commit_now:
            self.commit(delete=False)

        return item

    def delete_item(self, item, commit_now=True):
        item = self._check_item(item)

        self._queue_delete.append(item)
        if commit_now:
            self.commit(add=False)

    def _check_item(self, item: Model):
        if type(item) in [int, str]:
            item = self.query.get(item)

        if not isinstance(item, self.__model__):
            raise Exception("Item type(%s) isn't Collect(%s)." % (item.__class__.__name__, self.__model__.__name__))

        return item

    def commit(self, add=True, delete=True):
        from app import dh

        if add:
            for item in self._queue_add:
                dh.session.add(item)

        if delete:
            for item in self._queue_delete:
                dh.session.delete(item)

        dh.session.commit()

        if add:
            self._queue_add.clear()

        if delete:
            self._queue_delete.clear()
