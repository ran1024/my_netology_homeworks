#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_3_exceptions-1.py
#

def poland_arifmetic():
    operation = []
    while True:
        print("Необходимо ввести польскую нотацию для двух положительных чисел или 'q'.\n"
              "Можно использовать следующие операции:\n"
              "\t Сложение\n"
              "\t Вычитание\n"
              "\t Умножение\n"
              "\t Деление\n"
             "Например: + 2 2\n")
        operation = str(input("Введите польскую нотацию для двух положительных чисел: ")).split()
        if 'q' in operation:
            exit(0)
        assert operation[0] in ('+', '-', '*', '/'), 'Введена неверная арифметическая операция!!!'

        try:
            result = eval(operation[1] + operation[0] + operation[2])
            print("Вы ввели: {0}, Результат: {1}".format(operation, result))
        except IndexError:
            print("\nВы не ввели необходимого количества аргументов!!! Попробуйте снова.\n")
        except ZeroDivisionError:
            print("\nНа ноль делить нельзя!!! Попробуйте ещё раз.\n")
        except NameError:
            print("\nВы ввели недопустимое значение! Попробуйте снова.\n")
        except Exception:
            print("Как то всё не так. Всё не так как надо! ")

poland_arifmetic()
