#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import re
from contact import Contact, PhoneBook


def edit_book(num):
    print(book_list[num].list_contact())
    while True:
        print(f'a -добавить l -вывод всех контактов d -удалить s -поиск q -выход')
        command = input('\nВведите команду: ')
        if re.search(r'^[aldsq]?$', command) and command:
            if command =='q':
                return
            elif command == 'a':
                name = input('\nВведите имя: ')
                if name:
                    surname = input('Введите фамилию: ')
                    if surname:
                        phone = input('Введите номер телефона: ')
                        if phone:
                            elite = input('Введите избранный контакт: ')
                            print('\nДобавление дополнительной информации.')
                            try:
                                ph_nmbrs = input('Введите дополнительные тлф.номера через запятую: ') + ','
                                list_ph_nmbrs = [i.strip() for i in ph_nmbrs.split(',')]
                                adv_inf = input('Введите email и ссылки на соцсети через запятую: ')
                                dict_adv_inf = {str(k).strip(): str(v).strip() for [k, v] in
                                                [i.split('=') for i in adv_inf.split(',')]}
                                book_list[num].add_contact(name, surname, phone, elite,
                                                           *list_ph_nmbrs, **dict_adv_inf)
                            except Exception:
                                print('\nОшибка! Не удалось добавить контакт.\n'
                                      'Неправильный формат ввода дополнительной информации.\n'
                                      'Пример: telegram=@jhony, email=jhony@smith.com')
                print(book_list[num].list_contact())
            elif command == 'l':
                print(book_list[num].list_contact())
            elif command == 'd':
                phone = input('\nВведите номер телефона для удаления контакта: ')
                print(book_list[num].dell_contact(phone))
            elif command == 's':
                name = input('Введите имя контакта для поиска: ')
                surname = input('Введите фамилию контакта для поиска: ')
                print('\n{0:-^64}'.format(f'Поиск контакта: {name} {surname}'))
                print(book_list[num].search_contact(name, surname), '\n')
        else:
            print('Введена недопустимая команда!')


def print_header():
    print('\n{0:-^64}'.format('Программа Телефонная Книга'))
    i = 0
    for i, item in enumerate(book_list):
        print(f'{i} - {item.name_phone_book}')
    print('\n' * (20-i))
    print(f'n -новая тлф.книга  "номер" - открыть тлф.книгу  q -Выход')


def main():
    while True:
        print_header()
        command = input('\nВведите команду: ')
        if re.search(r'^[nq\d]?$', command) and command:
            if command =='q':
                return
            elif command == 'n':
                name = input('Введите имя новой телефонной книги: ')
                book_list.append(PhoneBook(name)) if name else print('\nВы ничего не ввели!')
            else:
                if int(command) < len(book_list):
                    edit_book(int(command))


if __name__ == '__main__':
    import sys
    sys.exit(main())
