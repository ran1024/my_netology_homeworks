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

    def set_additional_inf(self, *args, **kwargs):
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

    def __init__(self, name):
        self.name_phone_book = name
        self.contact_list = []

    def add_contact(self,  name, surname, phone, elite=False):
        contact = Contact(name, surname, phone, elite)
        self.contact_list.append(contact)

    def list_contact(self):
        for contact in self.contact_list:
            print(contact)

    def dell_contact(self, num):
        for contact in self.contact_list:
            if num == contact.phone:
                try:
                    self.contact_list.remove(contact)
                except ValueError:
                    print('Ошибка! Запись не найдена.')

    def search_contact(self, name, surname):
        for contact in self.contact_list:
            if surname == contact.surname and name == contact.name:
                print(contact)


def main():
    jhon = Contact('Jhon', 'Smith', '+71234567809')
    jhon.set_additional_inf(telegram='@jhony', email='jhony@smith.com')
    print(jhon)


if __name__ == '__main__':
    import sys
    sys.exit(main())
