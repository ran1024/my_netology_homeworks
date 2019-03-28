#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# example.py
#
# Программа переводит текстовый файл на русский язык (по умолчанию) или любой другой язык
# и сохраняет результат в новом файле.
# Принимает 3 обязательных параметра и 1 необязательный:
#         1. файл для перевода,
#         2. файл для записи результата,
#         3. язык текста первого файла,
#         4. язык на который надо сделать перевод (это необязательный параметр). По умолчанию равен "ru".
#

import sys
import requests

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


# Сделал своё исключение чтобы ловить ответ яндекса в случае неудачи.
class YandexAPIException(Exception): pass


def read_write_file(input_file, output_file, from_lang, to_lang):
    """
    Функция принимает входной и выходной файлы, языки с какого на какой переводить
    и производит перевод текста и его запись в выходной файл.
    :param input_file:
    :param output_file:
    :param from_lang:
    :param to_lang:
    """
    try:
        with open(input_file) as fh_in, open(output_file, 'w') as fh_out:
            fh_out.write(translate_it(fh_in.read(), from_lang, to_lang))
    except EnvironmentError as err:
        print('Error working with files:', err)


def translate_it(text, from_lang, to_lang):
    """
    Функция принимает текст для перевода, языки с какого на какой переводить
    и делает запрос в яндекс-перводчик.
    :param text:
    :param from_lang:
    :param to_lang:
    :return:
    """
    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{0}-{1}'.format(from_lang, to_lang),
        'options': 1
    }

    try:
        response = requests.post(URL, data=params)
        json_ = response.json()

        if response.status_code != 200:
            raise YandexAPIException()

        if json_['detected']['lang'] != from_lang:
            print('Вы не угадали с языком исходного файла. Яндекс решил что это "{}".'
                  .format(json_['detected']['lang']))

    except YandexAPIException:
        print('Yandex answer with code: {0} - {1}'.format(json_['code'], json_['message']))
    except requests.exceptions.RequestException as err:
        print('Requests error:', err)
    else:
        return ''.join(json_['text'])


def main():
    if len(sys.argv) <= 3 or sys.argv[1] in {"-h", "--help"}:
        print('usade: {0} input_file, output_file, language_of_input_file [language_of_output_file]'
              .format(sys.argv[0].rpartition("/")[2]))
        sys.exit(0)

    to_lang = 'ru' if len(sys.argv) <= 4 else sys.argv[4]
    input_file, output_file, from_lang = sys.argv[1:4]

    read_write_file(input_file, output_file, from_lang, to_lang)


main()

