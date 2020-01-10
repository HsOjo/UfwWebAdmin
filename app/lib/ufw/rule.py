class Rule:
    ACTION_ALLOW = 'ALLOW'
    ACTION_DENY = 'DENY'
    ACTION_REJECT = 'REJECT'
    ACTION_LIMIT = 'LIMIT'
    ACTIONS = []

    DIRECTION_IN = 'IN'
    DIRECTION_OUT = 'OUT'
    DIRECTION_FORWARD = 'FWD'
    DIRECTIONS = []

    ADDRESS_ANYWHERE = 'Anywhere'

    def __init__(self, src: str, dest: str, action: str, direction=DIRECTION_IN, is_v6: bool = False, src_eth=None,
                 dest_eth=None, comment=None, number=None, **kwargs):
        self.number = number
        self.src = src
        self.src_eth = src_eth
        self.dest = dest
        self.dest_eth = dest_eth
        self.action = action
        self.direction = direction
        self.comment = comment
        self.is_v6 = is_v6

    @property
    def data(self):
        attrs = list(set(dir(self)) - set(dir(Rule)))
        result = {}
        for k in attrs:
            if not callable(k):
                result[k] = getattr(self, k)

        return result

    def __repr__(self):
        return '<Rule %s>' % (' '.join('%s=%a' % (k, v) for k, v in self.data.items()))


Rule.ACTIONS = [getattr(Rule, k) for k in dir(Rule) if 'ACTION_' in k[:7]]
Rule.DIRECTIONS = [getattr(Rule, k) for k in dir(Rule) if 'DIRECTION_' in k[:10]]
