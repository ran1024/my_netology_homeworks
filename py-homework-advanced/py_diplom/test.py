#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import unittest
import VKinder


class VkinderTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(1, 2), 3)

    def test_sub(self):
        self.assertEqual(calc.sub(4, 2), 2)

    def test_mul(self):
        self.assertEqual(calc.mul(2, 5), 10)

    def test_div(self):
        self.assertEqual(calc.div(8, 4), 2)


if __name__ == '__main__':
    unittest.main()
