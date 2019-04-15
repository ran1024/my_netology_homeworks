#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import unittest
from unittest.mock import patch
from works import department


class TestDepartmentFuncs(unittest.TestCase):
    def setUp(self) -> None:
        self._documents = department.documents
        self._shelfs = department.directories

    def tearDown(self) -> None:
        del self._documents
        del self._shelfs

    def test_get_document(self):
        # Проверка корректного значения.
        number_of_document = '2207 876234'
        self.assertEqual(department.get_document(number_of_document), (0, 0))
        # Проверка несуществующего значения.
        number_of_document = 'НОМЕР'
        self.assertEqual(department.get_document(number_of_document),
                         (1, 'Документа с номером НОМЕР не существует!'))

    def test_get_shelf(self):
        number_of_document = '11-2'
        self.assertEqual(department.get_shelf(number_of_document), (0, '1'), 'Проверка корректного значения.')
        number_of_document = 'НОМЕР'
        self.assertEqual(department.get_shelf(number_of_document),
                         (1, 'Документа с данным номером нет на полках!'), 'Проверка несуществующего значения.')

    @patch('builtins.input', side_effect=['10006'])
    def test_get_people(self, mock):
        self.assertEqual(department.get_people(), 'Имя: Аристарх Павлов\n')

    def test_get_number_of_shelf(self):
        # введены корректные значения
        user_input = ['10006']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.get_number_of_shelf(), 'Документ 10006 находиться на полке: 2\n')
        # введён не корректный номер документа
        user_input = ['10000']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.get_number_of_shelf(), 'Документа с данным номером нет на полках!')

    @patch('builtins.input', side_effect=['555', 'passport', 'Ван Гог', '3'])
    def test_ok_add_document(self, mock):
        self.assertEqual(department.add_document(),
                         'Документ 555, добавлен на полку 3.\n')

    def test_err_add_document(self):
        user_input = ['', 'passport', 'Ван Гог', '3']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.add_document(), 'Введены недопустимые данные!\n')
        user_input = ['555', '', 'Ван Гог', '3']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.add_document(), 'Введены недопустимые данные!\n')
        user_input = ['555', 'passport', '', '3']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.add_document(), 'Введены недопустимые данные!\n')
        user_input = ['555', 'passport', 'Ван Гог', 'полка']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.add_document(), 'Введён недопустимый номер полки!\n')

    def test_del_document(self):
        # пользователь ввёл корректный номер документа
        user_input = ['33']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.del_document(), 'Документ 33 удалён.\n')
        # далее вводятся не корректные номера документа
        user_input = ['7']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.del_document(), 'Несуществующий документ: 7!\n')
        user_input = ['']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.del_document(), 'Несуществующий документ: !\n')

    def test_move_document(self):
        # введены корректные значения
        user_input = ['11-2', '3']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.move_document(), 'Документ 11-2 перемещён на полку 3.\n')
        # введён не корректный номер документа
        user_input = ['11-6', '3']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.move_document(), 'Несуществующий документ: 11-6!\n')
        # введён не корректный номер полки
        user_input = ['11-6', '9']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.move_document(), 'Введён недопустимый номер полки!\n')

    def test_add_shelf(self):
        # введено корректные значения полки
        user_input = ['4']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.add_shelf(), 'Полка № 4 добавлена.\n')
        # введён не корректный номер полки
        user_input = ['1']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(department.add_shelf(), 'Введён недопустимый номер полки!\n')


if __name__ == '__main__':
    unittest.main()
