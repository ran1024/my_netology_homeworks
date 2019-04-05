#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import re


class Contact(object):

    def __init__(self, name, surname, phone, elite=False):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.elite = elite if elite else 'нет'
        self.additional_num = set()
        self.additional_inf = {}

    def get_additional_inf(self, *args, **kwargs):
        """
        Добавление дополнительной информации:
        :param args: список дополнительных тлф.номеров
        :param kwargs: email, ссылки на соцсети
        """
        p = re.compile(r"^\+[0-9]+$")
        for num in args:
            if p.search(num):
                self.additional_num.add(num)
        for k, v in kwargs.items():
            self.additional_inf[k] = v

    def chg_elite(self, elite):
        self.elite = elite

    def __str__(self):
        result = (f'\nИмя: {self.name}'
                  f'\nФамилия: {self.surname}'
                  f'\nТелефон: {self.phone}'
                  f'\nВ избранных: {self.elite}'
                  f'\nДополнительная информация:\n\t')
        result += '\n\t'.join(f'{k} : {v}' for k, v in self.additional_inf.items())
        result += '\nДополнительные номера:'
        result += ', '.join(str(x) for x in self.additional_num)
        return result


class PhoneBook(object):
    pass


def main():
    pass


if __name__ == '__main__':
    import sys
    sys.exit(main())
