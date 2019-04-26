#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# tickets_for_concerts.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import csv
import re
from pymongo import MongoClient
from datetime import datetime


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    source_list = []
    with open(csv_file, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            concert = dict(row)
            dm = concert['Дата'].split('.')
            concert['Дата'] = datetime(2019, int(dm[1]), int(dm[0]))
            source_list.append(concert)
    db.insert_many(source_list)


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и вернуть их по возрастанию цены
    """
    pattern = re.escape(name)
    regex = re.compile(pattern, re.IGNORECASE)
    result = []
    for conc in db.find({'Исполнитель': regex}, {'_id': 0}).sort('Цена'):
        conc['Дата'] = conc['Дата'].strftime("%d.%m.%Y")
        result.append(conc)
    return result


def find_with_sort(db, sort_by=None):
    """
    Реализуем сортировку по произвольному ключу.
    """
    result = []
    if not sort_by:
        sort_by = '_id'
    for conc in db.find({}, {'_id': 0}).sort(sort_by):
        conc['Дата'] = conc['Дата'].strftime("%d.%m.%Y")
        result.append(conc)
    return result


def find_with_all(db, sort_by=None, name=None):
    """
    Реализуем сортировку по произвольному ключу и поиск
    по имени исполнителя (в том числе – по подстроке).
    Эта функция универсальна и заменяет предыдущие две.
    """
    result = []
    if not sort_by:
        sort_by = '_id'
    pattern = re.escape(name) if name else r'.*'
    regex = re.compile(pattern, re.IGNORECASE)
    for conc in db.find({'Исполнитель': regex}, {'_id': 0}).sort(sort_by):
        conc['Дата'] = conc['Дата'].strftime("%d.%m.%Y")
        result.append(conc)
    return result


def find_by_date(db, start_date=False, end_date=False):
    """
    Найти все мероприятия с начальной по конечную дату.
    """
    result = []
    for conc in db.find({'Дата': {'$lte': end_date, '$gte': start_date}}, {'_id': 0}).sort('Дата'):
        conc['Дата'] = conc['Дата'].strftime("%d.%m.%Y")
        result.append(conc)
    return result


def main():
    client = MongoClient()
    db = client.concerts
    artists = db.artists

    # Читаем csv из файла и пишем в базу MongoDB
    read_data('artists.csv', artists)

    # Получаем записи, отсортированные по цене.
    for i in find_with_all(artists, 'Цена'):
        print(i)

    print('\n')
    # Ищем билеты по имени исполнителя.
    for i in find_with_all(artists, name='Th'):
        print(i)

    print('\n')
    # Получаем записи, отсортированные по дате.
    for i in find_with_all(artists, 'Дата'):
        print(i)

    print('\n')
    # Находим все мероприятия с 1 по 30 июля.
    start_d = datetime(2019, 7, 1)
    end_d = datetime(2019, 7, 30)
    for i in find_by_date(artists, start_d, end_d):
        print(i)


if __name__ == '__main__':
    import sys
    sys.exit(main())
