import time


def convert_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
