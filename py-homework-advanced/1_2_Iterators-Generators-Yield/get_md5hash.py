#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# get_md5hash.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Создан генератор, который принимает путь к файлу.
# При каждой итерации возвращает md5 хеш каждой строки файла.
#
import hashlib


def get_md5hash(path):
    with open(path, 'r') as fh:
        while True:
            item = fh.readline()
            if not item:
                break
            yield hashlib.md5(item.encode('utf8')).hexdigest()


def main():
    for line in get_md5hash('countries.txt'):
        print(line)


if __name__ == '__main__':
    main()
