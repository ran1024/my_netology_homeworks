#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import unittest
import vkinder


class VkinderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.relation = {
            1: (4, 'в браке не состоит'),
            2: (2, 'есть друг или подруга'),
            5: (3, 'всё сложно'),
            6: (5, 'в активном поиске'),
        }
        cls.item = {
            'first_name': 'Vasia',
            'last_name': 'Pupkin',
            'photo_max_orig': 'aaa',
            'id': '1234',
            'relation': 1,
            'is_friend': 1,
            'common_count': 2,
        }
        cls.item_dict = {
            'Реципиент': f'{cls.item["first_name"]} {cls.item["last_name"]}',
            'Фотография': cls.item['photo_max_orig'],
            'Адрес в ВК': f'https://vk.com/id{cls.item["id"]}',
            'id': cls.item['id'],
            'select': 0,
            'Семейное положение': cls.relation[cls.item['relation']][1],
            'Является ли Вашим другом': 'да',
            'Количество общих друзей': cls.item['common_count'],
            'rating': 11
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def test_if_error(self):
        self.assertEqual(vkinder.if_error([0, 'Это тестовое сообщение']), 0)
        self.assertEqual(vkinder.if_error([1, 'Это тестовое сообщение']), 1)

    def test_prepare_user(self):
        self.assertDictEqual(vkinder.prepare_user(self.item, self.relation), self.item_dict)

    # def test_mul(self):
    #     self.assertEqual(calc.mul(2, 5), 10)
    #
    # def test_div(self):
    #     self.assertEqual(calc.div(8, 4), 2)


if __name__ == '__main__':
    unittest.main()
