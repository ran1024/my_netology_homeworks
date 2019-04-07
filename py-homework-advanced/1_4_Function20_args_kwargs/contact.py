#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# contact.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Модуль для применения в телефонной книге.
#
import re


class Contact(object):

    def __init__(self, name, surname, phone, elite=False, *args, **kwargs):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.elite = elite if elite else 'нет'
        self.additional_num = []
        self.additional_inf = {}
        p = re.compile(r"^\+?[0-9]+$")
        for num in args:
            if p.search(num):
                self.additional_num.append(num)
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
        self.contact_dict = {}

    def add_contact(self,  name, surname, phone, elite, *args, **kwargs):
        contact = Contact(name, surname, phone, elite, *args, **kwargs)
        self.contact_dict[phone] = contact

    def list_contact(self):
        result = '\n{0:-^64}'.format(self.name_phone_book)
        for key in self.contact_dict:
            result += self.contact_dict[key].__str__() + '\n'
        return result

    def dell_contact(self, num):
        if num in self.contact_dict:
            try:
                self.contact_dict.pop(num)
                return f'Контакт с номером {num} удалён.'
            except KeyError:
                return 'Ошибка! Запись не найдена.'
        else:
            return f'Контакта с номером телефона: {num} не существует.'

    def search_contact(self, name, surname):
        contact = False
        for val in self.contact_dict.values():
            if surname == val.surname and name == val.name:
                contact = val
        return contact if contact else 'Контакт не найден.'
