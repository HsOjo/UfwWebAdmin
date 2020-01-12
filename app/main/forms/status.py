from wtforms import SelectField, SubmitField

from app.base.form import Form
from app.lib import Ufw


class StatusForm(Form):
    status = SelectField(choices=[(i, i) for i in Ufw.STATUS_CHOICES])
    logging = SelectField(choices=[(i, i) for i in Ufw.LOGGING_CHOICES])
    logging_level = SelectField(choices=[(i, i) for i in Ufw.LOGGING_LEVEL_CHOICES])

    incoming = SelectField(choices=[(i, i) for i in Ufw.RULE_ACTION_CHOICES])
    outgoing = SelectField(choices=[(i, i) for i in Ufw.RULE_ACTION_CHOICES])
    routed = SelectField(choices=[(i, i) for i in Ufw.RULE_ACTION_CHOICES])

    submit = SubmitField(label='Submit')
