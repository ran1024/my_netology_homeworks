#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
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
        for key in self.contact_dict:
            print(self.contact_dict[key])

    def dell_contact(self, num):
        if num in self.contact_dict:
            try:
                self.contact_dict.pop(num)
            except KeyError:
                print('Ошибка! Запись не найдена.')
        else:
            print(f'Контакта с номером телефона: {num} не существует.')

    def search_contact(self, name, surname):
        for val in self.contact_dict.values():
            if surname == val.surname and name == val.name:
                print(val)


text_commands = f'a -добавить l -вывод всех контактов d -удалить s -поиск q -выход'
text_first = f'n -новая тлф.книга  "номер" - открыть тлф.книгу  q -Выход'
title1 = 'Программа Телефонная Книга'
book_list = []


def edit_book(num):
    while True:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{0:-^64}'.format(book_list[num].name_phone_book))
        print(book_list[num].list_contact())
        print(text_commands)
        command = input('\nВведите команду: ')
        if re.search(r'^[aldsq]?$', command) and command:
            if command =='q':
                return
            elif command == 'a':
                name = input('\nВведите имя: ')
                if name:
                    surname = input('\nВведите фамилию: ')
                    if surname:
                        phone = input('\nВведите номер телефона: ')
                        if phone:
                            elite = input('\nВведите избранный контакт: ')
                            print('Добавление дополнительной информации.')
                            try:
                                ph_nmbrs = input('\nВведите дополнительные тлф.номера через запятую: ')
                                list_ph_nmbrs = [i.strip() for i in ph_nmbrs.split(',')]
                                adv_inf = input('\nВведите email и ссылки на соцсети через запятую: ')
                                dict_adv_inf = {str(k).strip(): str(v).strip() for [k, v] in
                                                [i.split('=') for i in adv_inf.split(',')]}
                                book_list[num].add_contact(name, surname, phone, elite,
                                                           *list_ph_nmbrs, **dict_adv_inf)
                            except Exception:
                                print('\nОшибка! Не удалось добавить контакт.\n'
                                      'Неправильный формат ввода дополнительной информации.\n'
                                      'Пример: telegram=@jhony, email=jhony@smith.com')
            elif command == 'l':
                print(book_list[num].list_contact())
            elif command == 'd':
                phone = input('\nВведите номер телефона для удаления контакта: ')
                book_list[num].dell_contact(phone)
            elif command == 's':
                name = input('\nВведите имя контакта для поиска: ')
                surname = input('\nВведите фамилию контакта для поиска: ')
                book_list[num].search_contact(name, surname)
        else:
            print('Введена недопустимая команда!')


def print_header(title, text):
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{0:-^64}'.format(title))
    i = 0
    for i, item in enumerate(book_list):
        print(f'{i} - {item.name_phone_book}')
    print('\n' * (8-i))
    print(text)


def main():
    while True:
        print_header(title1, text_first)
        command = input('\nВведите команду: ')
        if re.search(r'^[nq\d]?$', command) and command:
            if command =='q':
                return
            elif command == 'n':
                name = input('Введите имя новой телефонной книги: ')
                book_list.append(PhoneBook(name)) if name else print('Вы ничего не ввели!')
            else:
                edit_book(int(command))


if __name__ == '__main__':
    import sys
    sys.exit(main())
