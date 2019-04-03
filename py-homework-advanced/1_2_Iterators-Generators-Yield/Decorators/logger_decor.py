#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Представлены 2 декоратора. Оба записывают в файл дату и время вызова функции,
# имя функции, аргументы, с которыми вызвалась и возвращаемое значение.
# Декоратор logger_with_param дополнительно принимает путь к логфайлу в качестве параметра.
#


def logger(funk):
    import datetime

    def wrapper(*args, **kwargs):
        dt_start = datetime.datetime.today()
        log = f'{dt_start.strftime("%X %d-%m-%Y")}, {funk.__name__}'
        log += '(' + ', '.join(['{0!r}'.format(i) for i in args] +
                               ['{0}={1!r}'.format(k, v) for k, v in kwargs.items()])
        result = exception = None
        try:
            result = funk(*args, **kwargs)
            return result
        except Exception as err:
            exception = err
        finally:
            log += ') -> ' + str(result) if exception is None else '{0}: {1}'.format(type(exception), exception)
            log += '\n'
            with open('decorators.log', 'a') as fh:
                fh.write(log)
        if exception is not None:
            raise exception
    return wrapper


def logger_with_param(path_to_file_name):
    def decorator(funk):
        import datetime

        def wrapper(*args, **kwargs):
            dt_start = datetime.datetime.today()
            log = f'{dt_start.strftime("%X %d-%m-%Y")}, {funk.__name__}'
            log += '(' + ', '.join(['{0!r}'.format(i) for i in args] +
                               ['{0}={1!r}'.format(k, v) for k, v in kwargs.items()])
            result = exception = None
            try:
                result = funk(*args, **kwargs)
                return result
            except Exception as err:
                exception = err
            finally:
                log += ') -> ' + str(result) if exception is None else '{0}: {1}'.format(type(exception), exception)
                log += '\n'
                with open(path_to_file_name, 'a') as fh:
                    fh.write(log)
            if exception is not None:
                raise exception
        return wrapper
    return decorator
