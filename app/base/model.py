from flask_sqlalchemy import BaseQuery, Model as RawModel


class Model(RawModel):
    query: BaseQuery

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __repr__(self):
        fields = []

        for k, v in self.__dict__.items():

            if k[0] != '_':

                if isinstance(v, Model):
                    fields.append('%s=<%s ...>' % (k, v.__class__.__name__))
                elif isinstance(v, str):
                    fields.append("%s='%s'" % (k, v))
                else:
                    fields.append('%s=%a' % (k, v))

        result = '<%s %s>' % (self.__class__.__name__, ' '.join(fields))
        return result
