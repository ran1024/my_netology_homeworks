#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# adv_print.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#


def adv_print(*args, start='', max_line=None, in_file=False, **kwargs):
    """
    Расширенная версия функции print()
    :param args: строка для печати.
    :param start: str() - с чего начинается вывод. По умолчанию пустая строка;
    :param max_line: int() - максимальная длина строки при выводе.
    :param in_file: bool -  определяет, будет ли записан вывод ещё и в файл: ./print.txt
    :param kwargs: служебные параметры штатной print()
    """
    sep = kwargs['sep'] if 'sep' in kwargs else ' '
    input_str = sep.join(str(a) for a in args)
    print_string = start + '\n'
    if max_line and len(input_str) > int(max_line):
        y = int(max_line)
        x = 0
        while x < len(input_str):
            print_string += f'{input_str[x:y]}\n'
            x = y
            y += int(max_line)
    else:
        print_string = input_str
    print(print_string, **kwargs)
    if in_file:
        with open('print.txt', 'w') as fh:
            fh.write(print_string)


adv_print('aaaaaaaaaabbbbbbbbbbqqqqqqqqqq', 'ccccccccccdddddddddd', start='QQ', max_line=30, in_file=True, sep="--")
