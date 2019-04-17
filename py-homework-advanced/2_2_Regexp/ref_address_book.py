#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ref_address_book.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Преобразование файла посредством регулярных выражений.
#
import re
import csv


def main():
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv") as fh:
        rows = csv.reader(fh, delimiter=",")
        contacts_list = list(rows)

    # стандартизируем телефонный номер
    p1 = re.compile(r'(\+?[7|8])\s?\(?(\d\d\d)\)?[-| ]?(\d+)[- ]?(\d\d)[- ]?(\d\d)\s+?\(?(доб\.)? ?(\d+)?\)?')
    # приводим весь файл к стандартному виду
    p2 = re.compile(r'''
        ([А-Я]\w+)\s                    # фамилия
        ([А-Я]\w+)\s                    # имя
        ([А-Я]\w+)?\s+                  # отчество
        ([А-Я]\w+)?\s+                  # место работы
        ([\w\s-]*)(?![+])\s+            # должность
        ([+\d\(\)\-]+\s(?:доб\.\d+)?)?  # телефон + добавочный если есть 
        (.+)?                           # email
        ''', re.VERBOSE)
    result_dict = {}
    result_list = [['Фамилия', 'Имя', 'Отчество', 'Место работы', 'Должность', 'Телефон', 'Эл.почта']]
    for item in contacts_list:
        str_entry = ' '.join(item)
        # print(str_entry)
        str_entry = p1.sub(r'+7(\2)\3-\4-\5 \6\7', str_entry)
        m = p2.findall(str_entry)
        if len(m):
            ss = []
            for i in m[0]:                          # удаляем лишние пробелы
                aa = i.strip()
                ss.append(aa)
            if ss[0] in result_dict:                # сводим вместе дублирующиеся записи
                for i, var in enumerate(ss):
                    if result_dict[ss[0]][i] == '':
                        result_dict[ss[0]][i] = var
            else:
                result_dict[ss[0]] = ss
                result_list.append(ss)              # результирующий список списков (используется тот факт,
                                                    #  что в список помещаются ссылки, а не сами объекты.
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w") as fh:
        datawriter = csv.writer(fh, delimiter=',')
        datawriter.writerows(result_list)


if __name__ == '__main__':
    import sys
    sys.exit(main())
