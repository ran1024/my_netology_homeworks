#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 3_1_formats.py
#
# Программа выводит 10 самых часто встречающихся в новостях слов длиннее 6 символов.
#
import xml.etree.ElementTree


def word_count_of_news(string, words):
    """
    Функция производит разбор строки по словам и пишет в словарь каждое слово и частоту его упоминания.
    """
    for word in string.lower().split():
        word = word.strip()
        if len(word) > 6:
            words[word] = words.get(word, 0) + 1


def main():
    words = {}

    tree = xml.etree.ElementTree.parse('newsafr.xml')

    for element in tree.findall('channel/item'):
        text = element.find('description').text
        if text:
            word_count_of_news(text.strip(), words)

    sort_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
    print("10 самых часто встречающихся слов длиннее 6 символов:")
    print("\n Слово          число повторений")
    print("--------------------------------")
    for i in range(10):
        print("{0:20} - {1}".format(sort_words[i][0], sort_words[i][1]))


main()
