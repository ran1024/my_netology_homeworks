#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# main.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#

from application import people
from application.salary import calculate_salary


def main():
    msg = calculate_salary()
    print(msg)
    msg1 = people.get_employees()
    print(msg1)


if __name__ == '__main__':
    main()
