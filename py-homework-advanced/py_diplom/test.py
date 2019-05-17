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

    # @classmethod
    def setUp(self) -> None:
        self.relation = {
            0: (1, 'не указано'),
            1: (4, 'в браке не состоит'),
            2: (2, 'есть друг или подруга'),
            3: (1, 'помолвлен / помолвлена'),
            4: (0, 'состоит в браке'),
            5: (3, 'всё сложно'),
            6: (5, 'в активном поиске'),
            7: (2, 'влюблён / влюблена'),
            8: (0, 'в гражданском браке')
        }
        self.item = {
            'first_name': 'Vasia',
            'last_name': 'Pupkin',
            'photo_max_orig': 'aaa',
            'id': '1234',
            'relation': 1,
            'is_friend': 1,
            'common_count': 2,
        }

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_if_error(self):
        self.assertEqual(vkinder.if_error([0, 'Это тестовое сообщение']), 0)
        self.assertEqual(vkinder.if_error([1, 'Это тестовое сообщение']), 1)

    def test_prepare_user(self):
        item_dict = {

        }
        self.assertEqual(vkinder.prepare_user(self.item, self.relation)['rating'], 11)

    # def test_mul(self):
    #     self.assertEqual(calc.mul(2, 5), 10)
    #
    # def test_div(self):
    #     self.assertEqual(calc.div(8, 4), 2)


if __name__ == '__main__':
    unittest.main()
