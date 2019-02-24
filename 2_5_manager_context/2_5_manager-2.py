#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_5_manager-2.py
#
# Применяем менеджер контекста из задания 1 (импорт модуля MyManagerCtxt).
# Программа "Кулинарная книга". Читатем рецепты из файла recipes.txt.
#
from pprint import pprint
from MyManagerCtxt import MyManagerCtxt


def read_recipes(cook_book, book_file):
    with MyManagerCtxt(book_file) as fh:
        headings = ('ingridient_name', 'quantity', 'measure')
        for line in fh:
            line = line.strip()
            cook_book[line] = []
            num = int(fh.readline())
            for i in range(num):
                contents = [x.strip() for x in fh.readline().split('|')]
                cook_book[line].append(dict(zip(headings, contents)))
            fh.readline()


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    """
    Получить словарь: ключи - названия ингредиентов, значение - словарь с их количетсвом для блюда.
    """
    shop_list = {}
    for dish in dishes:
        for ingr in cook_book[dish]:
            quantity = int(ingr['quantity']) * person_count
            if ingr['ingridient_name'] in shop_list:
                shop_list[ingr['ingridient_name']]['quantity'] += quantity
            else:
                shop_list[ingr['ingridient_name']] = {'measure': ingr['measure'], 'quantity': quantity}
    return shop_list


def main():
    book_file = 'recipes.txt'
    cook_book = {}
    read_recipes(cook_book, book_file)
    pprint(cook_book, width=100)
    dishes = ['Омлет', 'Фахитос']
    shop_list = get_shop_list_by_dishes(dishes, 2, cook_book)
    pprint(shop_list, width=100)


main()
