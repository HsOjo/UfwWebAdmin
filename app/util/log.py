import os
import sys
import time
from io import StringIO
from threading import Lock

from flask.helpers import get_env

from app.res.const import Const
from app.util import io_helper, object_convert


class Log:
    if get_env() == 'development':
        log_dir = os.path.expanduser('~/Library/Logs/')
    else:
        log_dir = '/var/log'

    path_log = '%s/%s.log' % (log_dir, Const.app_name)
    path_err = '%s/%s.err.log' % (log_dir, Const.app_name)

    io_log = StringIO()
    io_err = StringIO()
    replaces = {}
    lock_log = Lock()

    stdout: StringIO = None
    stderr: StringIO = None

    debug = False

    @staticmethod
    def init_app(keep_log=False, debug=False):
        Log.debug = debug

        mode = 'a' if keep_log else 'w+'
        Log.io_log = open(Log.path_log, mode)
        Log.io_err = open(Log.path_err, mode)

        # redirect stdout and stderr.
        Log.stdout, Log.stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = Log.io_log, Log.io_err

        if Log.debug:
            Log.debug_redirect()

    @staticmethod
    def debug_redirect():
        log_w = Log.io_log.write
        err_w = Log.io_log.write

        def bind_log_w(*args, **kwargs):
            log_w(*args, **kwargs)
            Log.stdout.write(*args, **kwargs)

        def bind_err_w(*args, **kwargs):
            err_w(*args, **kwargs)
            Log.stderr.write(*args, **kwargs)

        Log.io_log.write = bind_log_w
        Log.io_err.write = bind_err_w

    @staticmethod
    def set_replaces(replaces: dict):
        Log.replaces = replaces

    @staticmethod
    def extract_log():
        with Log.lock_log:
            log = io_helper.read_all(Log.io_log, '')
        return log

    @staticmethod
    def extract_err():
        err = io_helper.read_all(Log.io_err, '')
        return err

    @staticmethod
    def append(src, tag='Info', *args):
        log_items = []
        for i in args:
            if isinstance(i, list) or isinstance(i, dict):
                log_items.append(object_convert.to_json(i))
            elif isinstance(i, tuple) or isinstance(i, set):
                log_items.append(object_convert.to_json(list(i)))
            elif isinstance(i, int) or isinstance(i, float) or isinstance(i, str) or isinstance(i, bool) or i is None:
                log_items.append(i)
            else:
                log_items.append(i)
                log_items.append(object_convert.to_json(object_convert.object_to_dict(i)))

        if isinstance(src, str):
            source = src
        else:
            source = src.__name__

        items_str = []
        for item in log_items:
            item_str = str(item)
            if len(Log.replaces) > 0:
                for k, v in Log.replaces.items():
                    if k is not None and k != '':
                        item_str = item_str.replace(k, v)

            items_str.append(item_str)

        items_str = ' '.join(items_str)
        if items_str.strip() != '':
            items_str = '\t%s\n' % items_str

        with Log.lock_log:
            content = '[%s] %s %s\n%s' % (tag, time.ctime(), source, items_str)
            Log.io_log.write(content)
            Log.io_log.flush()
