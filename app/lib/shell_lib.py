from app import common


class ShellLib:
    def __init__(self, path):
        self.path = path

    def exec_out(self, *args, **kwargs):
        return common.execute_get_out([self.path, *args], **kwargs)

    def exec(self, *args, **kwargs):
        return common.execute([self.path, *args], **kwargs)

    def popen(self, *args, **kwargs):
        return common.popen([self.path, *args], **kwargs)

    def inject_simple_command(self, func, *args, **kwargs):
        def func_new():
            [stat, out, err] = self.exec(func.__name__, *args, **kwargs)
            return stat == 0

        setattr(self, func.__name__, func_new)
