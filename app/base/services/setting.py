from app.base.service import Service
from app.base.models import SettingModel


class SettingService(Service):
    __model__ = SettingModel
