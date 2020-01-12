from flask_wtf import FlaskForm
from wtforms.csrf.core import CSRFTokenField


class Form(FlaskForm):
    data: dict
    csrf_token: CSRFTokenField

    def inject_data(self, **kwargs):
        for k, v in kwargs.items():
            item = getattr(self, k, None)
            if item is not None:
                setattr(item, 'data', v)
