import logging


def string_to_mode(string):
    res = None
    if string[0] == 's':
        res = logging.CRITICAL
    elif string[0] == 'w':
        res = logging.WARNING
    elif string[0] == 'i':
        res = logging.INFO
    return res
