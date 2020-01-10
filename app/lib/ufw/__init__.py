import re
from typing import List

from app import common
from app.lib.shell_lib import ShellLib
from app.lib.ufw.rule import Rule


class Ufw(ShellLib):
    RULE_ACTION_ALLOW = 'allow'
    RULE_ACTION_DENY = 'deny'
    RULE_ACTION_REJECT = 'reject'
    RULE_ACTION_LIMIT = 'limit'

    RULE_DIRECTION_IN = 'in'
    RULE_DIRECTION_OUT = 'out'

    RULE_LOG = 'log'
    RULE_LOG_ALL = 'log-all'
    RULE_ADDRESS_ANY = 'any'

    DEFAULT_DIRECTION_INCOMING = 'incoming'
    DEFAULT_DIRECTION_OUTGOING = 'outgoing'
    DEFAULT_DIRECTION_ROUTED = 'routed'

    LOGGING_LEVEL_OFF = 'off'
    LOGGING_LEVEL_ON = 'on'
    LOGGING_LEVEL_LOW = 'low'
    LOGGING_LEVEL_MEDIUM = 'medium'
    LOGGING_LEVEL_HIGH = 'high'
    LOGGING_LEVEL_FULL = 'full'

    STATUS_OPTION_VERBOSE = 'verbose'
    STATUS_OPTION_NUMBERED = 'numbered'

    def __init__(self, path=None):
        if path is None:
            path = common.execute_get_out(['which', 'ufw'])
            if path == '':
                raise FileNotFoundError("Couldn't find ufw.")

        super().__init__(path)

    def enable(self):
        out = self.exec_out('enable')
        return 'enabled' in out

    def disable(self):
        out = self.exec_out('disable')
        return 'disabled' in out

    def reload(self):
        out = self.exec_out('reload')
        return 'reloaded' in out

    def default(self, rule, direction=DEFAULT_DIRECTION_INCOMING):
        out = self.exec_out('default', rule, direction)
        return 'changed' in out

    def logging(self, level):
        if isinstance(level, bool):
            if level:
                out = self.exec_out('logging', Ufw.LOGGING_LEVEL_ON)
                return 'enabled' in out
            else:
                out = self.exec_out('logging', Ufw.LOGGING_LEVEL_OFF)
                return 'disabled' in out
        elif isinstance(level, str):
            out = self.exec_out('logging', level)
            return 'enabled' in out

        return False

    def reset(self):
        [stat, out, err] = self.exec('reset')
        return stat == 0

    def status(self, option=STATUS_OPTION_VERBOSE):
        out = self.exec_out('status', option)

        status = {}
        rules = []

        reg_option = re.compile('^(?P<key>.*?)\s*:\s*(?P<value>.*?)\s*$')
        reg_default = re.compile('(\S+) \((\S+)\)')
        reg_rule = re.compile(
            '^(\[\s*(?P<number>\d+)\])?(?P<dest>\S+)(\son\s(?P<dest_eth>\S+))?\s?(?P<dest_v6>\(v6\))?\s+(?P<action>\S+)(\s(?P<direction>\S+))?\s+(?P<src>\S+)\s?(\son\s(?P<src_eth>\S+))?(?P<src_v6>\(v6\))?\s*(#\s*(?P<comment>.*))?$')
        reg_cur = reg_option

        lines = out.split('\n')  # type: List[str]
        for line in lines:
            line = line.strip()
            if line != '':
                if reg_cur == reg_option:
                    data = reg_cur.match(line)
                    if data is not None:
                        data = data.groupdict()
                        status[data['key']] = data['value']
                    else:
                        reg_cur = reg_rule
                elif reg_cur == reg_rule:
                    data = reg_cur.match(line)
                    if data is not None:
                        data = data.groupdict()
                        if data['action'] in Rule.ACTIONS:
                            data['direction'] = data.get('direction', Rule.DIRECTION_IN)
                            data['is_v6'] = (data['src_v6'] or data['dest_v6']) is not None
                            rules.append(Rule(**data))

        if len(rules) > 0:
            status['Rules'] = rules

        logging = status.get('Logging')
        if logging is not None:
            result = reg_default.findall(logging)
            if result is not None:
                [(logging, level)] = result
                status['Logging'] = logging
                status['LoggingLevel'] = level

        default = status.get('Default')
        if default is not None:
            items = reg_default.findall(default)
            if items is not None:
                items = dict([(k, v) for v, k in items])
            status['Default'] = items

        return status

    @staticmethod
    def generate_rule(action, src=RULE_ADDRESS_ANY, dest=RULE_ADDRESS_ANY, direction=RULE_DIRECTION_IN, log: str = None,
                      protocol: str = None, comment: str = None, in_on_eth: str = None, out_on_eth: str = None):
        if in_on_eth is not None:
            in_on_eth = '%s on %s' % (Ufw.RULE_DIRECTION_IN, in_on_eth)
        if out_on_eth is not None:
            out_on_eth = '%s on %s' % (Ufw.RULE_DIRECTION_OUT, out_on_eth)
        if in_on_eth is not None and out_on_eth is not None:
            direction = None

        rule_args = [action, direction, in_on_eth, out_on_eth, log, protocol, 'from', src, 'to', dest, comment]
        rule_args = [arg for arg in rule_args if arg != '' and arg is not None]
        return rule_args

    @staticmethod
    def generate_rule_by_object(rule: Rule, **kwargs):
        data = rule.data.copy()
        if data['src'] == Rule.ADDRESS_ANYWHERE:
            data['src'] = Ufw.RULE_ADDRESS_ANY
        if data['dest'] == Rule.ADDRESS_ANYWHERE:
            data['dest'] = Ufw.RULE_ADDRESS_ANY

        data['in_on_eth'] = data.pop('src_eth')
        data['out_on_eth'] = data.pop('dest_eth')
        data['action'] = data['action'].lower()
        data['direction'] = data['direction'].lower()

        data.pop('is_v6')
        data.update(**kwargs)
        return Ufw.generate_rule(**data)

    def delete(self, rule):
        out = self.exec_out('delete', rule)
        return 'deleted' in out

    def add(self, rule):
        out = self.exec_out('add', rule)
        return 'added' in out

    def insert(self, num, rule):
        out = self.exec_out('insert', num, rule)
        return 'inserted' in out

    def prepend(self, num, rule):
        out = self.exec_out('prepend', num, rule)
        return 'inserted' in out
