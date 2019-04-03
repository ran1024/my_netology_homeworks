#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#


def logger1(funk):
    import datetime

    def wrapper(*args, **kwargs):
        dt_start = datetime.datetime.today()
        log = f'{dt_start.strftime("%X %d-%m-%Y")}, функция: {funk.__name__}'
        log += '(' + ', '.join(['{0!r}'.format(i) for i in args] +
                               ['{0}={1!r}'.format(k, v) for k, v in kwargs.items()])
        result = exception = None
        try:
            result = funk(*args, **kwargs)
            return result
        except Exception as err:
            exception = err
        finally:
            dt_end = datetime.datetime.today()
            log += ') -> ' + str(result) if exception is None else '{0}: {1}'.format(type(exception), exception)
            print(log)
        if exception is not None:
            raise exception
    return wrapper


@logger1
def qwerty(a1, a2=None):
    return a1, a2


print(qwerty(2, a2='йфяч вв'))
