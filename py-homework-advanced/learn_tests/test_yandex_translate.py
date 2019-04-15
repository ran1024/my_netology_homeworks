#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# yandex_translate.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import requests
import unittest
# from unittest.mock import patch

# API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'


def translate_it(text, from_lang, to_lang):
    """
    Функция принимает текст для перевода, языки с какого на какой переводить
    и делает запрос в яндекс-перводчик.
    :param text:
    :param from_lang:
    :param to_lang:
    :return:
    """
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    API_KEY = 'trnsl.1.1.20190302T010836Z.a4d0411e314ff791.de1924c3a95aace515ca6b366d7a06ebfde52424'

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
            return json_['code']
    except requests.exceptions.RequestException as err:
        return 'Requests error:', err
    else:
        return ''.join(json_['text'])


class TestDepartmentFuncs(unittest.TestCase):

    def test_ok_translate_it(self):
        # Проверка корректного значения.
        self.assertEqual(translate_it('помидор', 'ru', 'en'), 'tomato')

    def test_err_translate_it(self):
        # Проверка несуществующего значения языка.
        self.assertEqual(translate_it('помидор', 'uu', 'en'), 501)


if __name__ == '__main__':
    unittest.main()

