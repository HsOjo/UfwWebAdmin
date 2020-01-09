import os
import time
import traceback
from io import StringIO
from subprocess import PIPE, Popen, TimeoutExpired


def popen(cmd, sys_env=True, **kwargs):
    if isinstance(cmd, list):
        for i in range(len(cmd)):
            if not isinstance(cmd[i], str):
                cmd[i] = str(cmd[i])

    if sys_env and kwargs.get('env') is not None:
        kwargs['env'] = os.environ.copy().update(kwargs['env'])
    return Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8', **kwargs)


def execute(cmd, input_str=None, timeout=None, **kwargs):
    p = popen(cmd, **kwargs)
    try:
        out, err = p.communicate(input_str, timeout=timeout)
    except TimeoutExpired:
        out = ''
        err = get_exception()
        p.kill()
    stat = p.returncode
    return stat, out, err


def execute_get_out(cmd, **kwargs):
    [_, out, _] = execute(cmd, **kwargs)
    return out


def get_exception():
    with StringIO() as io:
        traceback.print_exc(file=io)
        io.seek(0)
        content = io.read()

    return content


def time_count(func):
    def core(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print('%s time usage: %f' % (func.__name__, time.time() - t))
        return result

    return core
