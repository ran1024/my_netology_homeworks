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


def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастания цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    result = []
    for conc in db.find({}, {'_id': 0}).sort('Цена'):
        conc['Дата'] = conc['Дата'].strftime("%d.%m.%Y")
        result.append(conc)
    return result


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и вернуть их по возрастанию цены
    """

    regex = re.compile('укажите регулярное выражение для поиска. ' \
                       'Обратите внимание, что в строке могут быть специальные символы, их нужно экранировать')


def main():
    client = MongoClient()
    db = client.concerts
    artists = db.artists
    # Читаем csv из файла и пишем в базу MongoDB
    # read_data('artists.csv', artists)
    # Получаем записи, отсортированные по цене.
    for i in find_cheapest(artists):
        print(i)


if __name__ == '__main__':
    import sys
    sys.exit(main())
