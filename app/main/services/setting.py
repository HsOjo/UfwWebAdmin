from app.base import Service
from app.main.models import SettingModel


class SettingService(Service):
    __model__ = SettingModel
