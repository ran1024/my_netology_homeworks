#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# adv_print.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Реализацию функции print - adv_print. Может получать три новых необязательных аргумента:
# start - с чего начинается вывод. По умолчанию пустая строка;
# max_line - максимальная длина строки при выводе. Если строка превыщает max_line, то вывод
# автоматически переносится на новую строку;
# in_file - аргумент, определяющий будет ли записан вывод ещё и в файл.
#


def adv_print(*args, start='', max_line=None, in_file=False, **kwargs):
    """
    Расширенная версия функции print()
    :param args: строка для печати.
    :param start: str() - с чего начинается вывод. По умолчанию пустая строка;
    :param max_line: int() - максимальная длина строки при выводе.
    :param in_file: bool -  определяет, будет ли записан вывод ещё и в файл.
    :param kwargs: служебные параметры штатной print()
    :return:
    """
    print(locals())
    sep = kwargs['sep'] if 'sep' in kwargs else ' '
    print_string = sep.join(str(a) for a in args)
    print(start)
    if max_line and len(print_string) > int(max_line):
        y = int(max_line)
        x = 0
        while x < len(print_string):
            print(print_string[x:y], **kwargs)
            x = y
            y += int(max_line)


adv_print('aaaaaaaaaabbbbbbbbbbqqqqqqqqqq', 'ccccccccccddddddddddeeeee', max_line=10, sep="--", flush=True)
