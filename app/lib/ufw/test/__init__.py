import os

from app.lib import Ufw, ShellLib

TEST_DIR = os.path.dirname(__file__)


class UfwTest(Ufw):
    def __init__(self):
        super(ShellLib).__init__()

    def exec(self, *args, **kwargs):
        stat = 0
        out = ''
        err = ''

        return stat, out, err

    def exec_out(self, *args: str, **kwargs):
        out = ''

        if args[0] in ['delete', 'add', 'insert']:
            out = 'Rule %sed' % (args[0] if args[0] != 'prepend' else 'insert')
        elif args[0] == 'default':
            out = '''Default incoming policy changed to '%s'
        (be sure to update your rules accordingly)''' % args[1]
        elif args[0] in ['enable', 'disable', 'reload']:
            out = '''Firewall %sed''' % (args[1].rstrip('e'))
        elif args[0] == 'logging':
            out = 'Logging %s' % ('disabled' if args[1] == Ufw.LOGGING_LEVEL_OFF else 'enabled')
        elif args[0] == 'status':
            if len(args) <= 1:
                with open('%s/%s' % (TEST_DIR, 'status.txt')) as io:
                    out = io.read()
            elif args[1] == Ufw.STATUS_OPTION_VERBOSE:
                with open('%s/%s' % (TEST_DIR, 'status_verbose.txt')) as io:
                    out = io.read()
            elif args[1] == Ufw.STATUS_OPTION_NUMBERED:
                with open('%s/%s' % (TEST_DIR, 'status_numbered.txt')) as io:
                    out = io.read()

        return out
