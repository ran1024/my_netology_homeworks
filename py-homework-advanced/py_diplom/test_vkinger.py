#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_vkinder.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Тестируем модуль vkinder
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
        cls.vkuser = vkinder.Vkinder()

    def test_if_error(self):
        self.assertEqual(vkinder.if_error([0, 'Это тестовое сообщение']), 0)
        self.assertEqual(vkinder.if_error([1, 'Это тестовое сообщение']), 1)

    def test_prepare_user(self):
        self.assertDictEqual(vkinder.prepare_user(self.item, self.relation), self.item_dict)

    def test_calculate_offset_1(self):
        """Проверяем, что при счётчике месяцев > 12 происходит переключение на 1 января."""
        self.vkuser.age_current = [1, 13]
        vkinder.calculate_offset(self.vkuser)
        self.assertListEqual(self.vkuser.age_current, [1, 1])

    def test_calculate_offset_2(self):
        """Проверяем, что при окончании февраля происходит переход на 1 марта."""
        self.vkuser.age_current = [29, 2]
        vkinder.calculate_offset(self.vkuser)
        self.assertListEqual(self.vkuser.age_current, [1, 3])

    def test_calculate_offset_3(self):
        """Проверяем, что при окончании месяца №4,6,9,11 происходит переход на 1 число следующего месяца."""
        for i in [4, 6, 9, 11]:
            self.vkuser.age_current = [31, i]
            vkinder.calculate_offset(self.vkuser)
            self.assertListEqual(self.vkuser.age_current, [1, i + 1])

    def test_calculate_offset_4(self):
        """Проверяем, что при окончании месяца №1,2,3,5,7,8,10,12 происходит переход на 1 число следующего месяца."""
        for i in [1, 2, 3, 5, 7, 8, 10, 12]:
            self.vkuser.age_current = [32, i]
            vkinder.calculate_offset(self.vkuser)
            self.assertListEqual(self.vkuser.age_current, [1, i + 1])

    def test_calculate_offset_5(self):
        """Проверяем, возвращаемое значение при окончании поиска."""
        self.age_min = 1997
        self.age_max = 1998
        self.assertTrue(vkinder.calculate_offset(self.vkuser))


if __name__ == '__main__':
    unittest.main()
