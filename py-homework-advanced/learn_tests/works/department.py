#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# department.py
# Домашнее задание к лекции 2.1 «Функции — использование встроенных и создание собственных»
#

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "insurance", "number": "33", "name": "Пабло Пикассо"},
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': ['33']
}


def get_document(number_of_document):
    """
    Возвращает индекс словаря содержащего нужный документ.
    """
    for i, items in enumerate(documents):
        if items['number'] == number_of_document:
            return 0, i
    return 1, f'Документа с номером {number_of_document} не существует!'


def get_shelf(number_of_document):
    """
    Возвращает номер полки с нужным номером документа.
    """
    for key, value in directories.items():
        if number_of_document in value:
            return 0, key
    return 1, 'Документа с данным номером нет на полках!'


def get_people():
    number_of_document = input('Введите номер документа: ')
    err, i = get_document(number_of_document)
    if not err:
        return f'Имя: {documents[i]["name"]}\n'
    else:
        return f'Бракованая запись. Нет поля "name" у документа {number_of_document}!\n'


def get_list():
    result = 'Список документов:\n'
    for items in documents:
        result += '{0} "{1}" "{2}"'.format(*items.values()) + '\n'
    return result


def get_number_of_shelf():
    number_of_document = input('Введите номер документа: ')
    err, shelf = get_shelf(number_of_document)
    if not err:
        return f'Документ {number_of_document} находиться на полке: {shelf}\n'
    else:
        return 'Документа с данным номером нет на полках!'


def add_document():
    number_of_document = input('Введите номер документа: ')
    type_of_document = input('Введите тип документа: ')
    name_owner = input('Введите ФИО владельца: ')
    if number_of_document == '' or type_of_document == '' or name_owner == '':
        return 'Введены недопустимые данные!\n'
    shelf_number = input('Введите номер полки: ')
    if shelf_number.isdigit() and shelf_number in directories.keys():
        documents.append({"type": type_of_document, "number": number_of_document, "name": name_owner})
        directories[shelf_number] += [number_of_document]
        return f'Документ {number_of_document}, добавлен на полку {shelf_number}.\n'
    else:
        return 'Введён недопустимый номер полки!\n'


def del_document():
    number_of_document = input('Введите номер документа: ')
    err, shelf = get_shelf(number_of_document)
    try:
        directories[shelf].remove(number_of_document)
        err, i = get_document(number_of_document)
        documents.pop(i)
        return f'Документ {number_of_document} удалён.\n'
    except (KeyError, ValueError):
        return f'Несуществующий документ: {number_of_document}!\n'


def move_document():
    """
    Функция перемещает документ на другую полку.
    """
    number_of_document = input('Введите номер документа: ')
    err, shelf = get_shelf(number_of_document)
    new_shelf = input('Введите номер полки: ')
    if new_shelf.isdigit() and new_shelf in directories.keys():
        try:
            directories[shelf].remove(number_of_document)
            directories[new_shelf].append(number_of_document)
            return f'Документ {number_of_document} перемещён на полку {new_shelf}.\n'
        except (KeyError, ValueError):
            return f'Несуществующий документ: {number_of_document}!\n'
    else:
        return 'Введён недопустимый номер полки!\n'


def add_shelf():
    new_shelf = input('Введите номер новой полки: ')
    if new_shelf.isdigit() and new_shelf not in directories.keys():
        directories[new_shelf] = []
        return f'Полка № {new_shelf} добавлена.\n'
    else:
        return 'Введён недопустимый номер полки!\n'


def print_all_people():
    """
    Функция выводит имена всех владельцев документов.
    """
    result = ''
    try:
        for items in documents:
            result += items['name'] + '\n'
        return result
    except KeyError:
        return f'Бракованая запись. Нет поля "name" у документа {items}!\n'


def main():
    commands = dict(p=get_people, l=get_list, s=get_number_of_shelf, a=add_document,
                    d=del_document, m=move_document, ads=add_shelf, pa=print_all_people)
    print(
        '\nКоманды: p - people,\n\t\t pa - print all people,\n\t\t l - list,\n\t\t s - shelf,\n'
        '\t\t a - add document,\n\t\t d - dell document,\n\t\t m - move document,\n\t\t ads - add shelf')
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            return
        elif command in commands.keys():
            result = commands[command]()
            print(f'\n{result}')
        else:
            print('Введена недопустимая команда!')


if __name__ == '__main__':
    import sys
    sys.exit(main())
