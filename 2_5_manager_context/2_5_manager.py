#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_5_manager.py
#
# Реализован менеджер контекста, печатающий на экран время запуска кода в менеджере контекста,
# время окончания работы кода и сколько времени было потрачено на выполнение кода.
#

from time import sleep
import datetime


class MyManager:

    def __init__(self, file_path):
        self.file_path = file_path
        self.time_start = datetime.datetime.now()

    def __enter__(self):
        self.file = open(self.file_path)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        self.time_stop = datetime.datetime.now()
        print('Время запуска кода:    ', self.time_start)
        print('Время окончания работы:', self.time_stop)
        print('На выполнение кода было потрачено: {0} сек.'.format(self.time_stop - self.time_start))


with MyManager('LICENSE') as fh:
    for line in fh:
        print(line)
        sleep(0.01)

