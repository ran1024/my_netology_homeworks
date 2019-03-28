#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_3_exceptions-2.py
# Домашнее задание к лекции 2.1 «Функции — использование встроенных и создание собственных»
#

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "insurance", "number": "12",},
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def get_document(number_of_document):
    """
    Возвращает индекс словаря содержащего нужный документ.
    """
    for i, items in enumerate(documents):
        if items['number'] == number_of_document:
            return i
    print('Документа с данным номером не существует!')
    exit(0)


def get_shelf(number_of_document):
    """
    Возвращает номер полки с нужным номером документа.
    """
    for key, value in directories.items():
        if number_of_document in value:
            return key
    print('Документа с данным номером нет на полках!')
    exit(0)


def get_people():
    try:
        number_of_document = input('Введите номер документа: ')
        i = get_document(number_of_document)
        print('Имя: ', documents[i]['name'], '\n')
    except KeyError:
        print("Бракованая запись. Нет поля 'name' у документа {}!\n".format(number_of_document))


def get_list():
    print('Список документов:')
    try:
        for items in documents:
            print('{0} "{1}" "{2}"'.format(*items.values()))
        print('\n')
    except IndexError:
        print("Бракованая запись. Нет поля 'name' у документа {}!\n".format(items))

#  print(directories)


def get_number_of_shelf():
    number_of_document = input('Введите номер документа: ')
    shelf = get_shelf(number_of_document)
    print('Документ {0} находиться на полке: {1}\n'.format(number_of_document, shelf))


def add_document():
    number_of_document = input('Введите номер документа: ')
    type_of_document = input('Введите тип документа: ')
    name_owner = input('Введите ФИО владельца: ')
    if number_of_document == '' or type_of_document == '' or name_owner == '':
        print('Введены недопустимые данные!\n')
        return
    shelf_number = input('Введите номер полки: ')
    if shelf_number.isdigit() and shelf_number in directories.keys():
        documents.append({"type": type_of_document, "number": number_of_document, "name": name_owner})
        directories[shelf_number] += [number_of_document]
        print('\nДокумент', number_of_document, 'добавлен на', shelf_number, 'полку.\n')
    else:
        print('Введён недопустимый номер полки!\n')


def del_document():
    number_of_document = input('Введите номер документа: ')
    shelf = get_shelf(number_of_document)
    directories[shelf].remove(number_of_document)
    i = get_document(number_of_document)
    documents.pop(i)
    print('Документ {0} удалён.\n'.format(number_of_document))


def move_document():
    number_of_document = input('Введите номер документа: ')
    shelf = get_shelf(number_of_document)
    new_shelf = input('Введите номер полки: ')
    if new_shelf.isdigit() and new_shelf in directories.keys():
        directories[shelf].remove(number_of_document)
        directories[new_shelf].append(number_of_document)
        print('Документ {0} перемещён на полку {1}.\n'.format(number_of_document, new_shelf))
    else:
        print('Введён недопустимый номер полки!\n')


def add_shelf():
    new_shelf = input('Введите номер новой полки: ')
    if new_shelf.isdigit() and new_shelf not in directories.keys():
        directories[new_shelf] = []
        print('Полка №', new_shelf, 'добавлена.\n')
    else:
        print('Введён недопустимый номер полки!\n')


def print_all_people():
    """
    Функция выводит имена всех владельцев документов.
    """
    try:
        for items in documents:
            print(items['name'])
        print('\n')
    except KeyError:
        print("Бракованая запись. Нет поля 'name' у документа {}!\n".format(items))


def main():
    commands = dict(p=get_people, l=get_list, s=get_number_of_shelf, a=add_document,
                    d=del_document, m=move_document, ads=add_shelf, pa=print_all_people)
    print(
        '\nКоманды: p - people,\n\t\t pa - print all people,\n\t\t l - list,\n\t\t s - shelf,\n'
        '\t\t a - add document,\n\t\t d - dell document,\n\t\t m - move document,\n\t\t ads - add shelf')
    while (True):
        command = input('Введите команду: ')
        if command == 'q':
            return
        elif command in commands.keys():
            commands[command]()
        else:
            print('Введена недопустимая команда!')


main()
