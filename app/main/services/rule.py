from app import Service
from app.main.models import RuleModel


class RuleService(Service):
    __model__ = RuleModel
