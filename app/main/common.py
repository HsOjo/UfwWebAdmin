import time

from app import load_setting, save_setting
from app.lib import Ufw, Rule
from app.main.services.rule import RuleService


def ufw_status(ufw: Ufw, expire_time=60):
    now = time.time()
    status = load_setting('ufw_status')  # type: dict
    if status is None:
        status = ufw.status(parse_rule=False)
    elif now - status.get('status_time', 0) >= expire_time:
        status.update(**ufw.status(parse_rule=False))
    else:
        return status

    status['status_time'] = now
    save_setting('ufw_status', status)

    return status


def ufw_sync_rule(ufw: Ufw):
    now = time.time()

    service = RuleService()
    for item in service.query.all():
        service.delete_item(item, commit_now=False)

    status = ufw.status()
    status['status_time'] = now
    status['rules_time'] = now

    rules = status.pop('rules')
    save_setting('ufw_status', status)

    for rule in rules:  # type: Rule
        service.add_item(commit_now=False, **rule.data)

    service.commit()
