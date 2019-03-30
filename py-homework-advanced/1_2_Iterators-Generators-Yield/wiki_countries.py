#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# wiki_countries.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Создаётся класс итератора, который для каждой страны из файла FILE_INPUT ищет страницу в википедии.
# После чего записывает в файл FILE_OUTPUT пару: страна – ссылка.
#

import wikipedia
import json

FILE_INPUT = 'countries.json'
FILE_OUTPUT = 'countries.txt'


class MyWikiCountries:

    def __init__(self, path):
        self.countries_common = []
        self.countries_official = []
        self.index = -1
        wikipedia.set_lang("ru")
        with open(path, 'r') as fh:
            self.data = json.load(fh)
        for item in self.data:
            self.countries_official.append(item['translations']['rus']['official'])
            self.countries_common.append(item['translations']['rus']['common'])

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.countries_common):
            raise StopIteration
        country = self.countries_official[self.index]
        try:
            complete_url = wikipedia.page(country)
            return f'{country} - {complete_url.url}'
        except (wikipedia.PageError, wikipedia.DisambiguationError):
            complete_url = wikipedia.page(self.countries_common[self.index])
            return f'{country} - {complete_url.url}'


def main():
    with open(FILE_OUTPUT, 'w') as fh:
        for item in MyWikiCountries(FILE_INPUT):
            print(item)
            fh.write(f'{item}\n')
            fh.flush()


if __name__ == '__main__':
    import sys
    sys.exit(main())
