import json

from app.main.services import SettingService


def load_setting(key: str):
    item = SettingService().get_items(key=key).first()
    if item is not None:
        return json.loads(item.value)
    return None


def save_setting(key: str, value):
    value = json.dumps(value, ensure_ascii=False)
    SettingService().add_item(key=key, value=value)
