#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dbworker.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
from pymongo import MongoClient
from datetime import datetime


class UseDB:
    """
    Здесь собраны все средства для работы с базой данных.
    """
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.vkinder
        self.vkowners = self.db.vkowners
        self.vkusers = self.db.vkusers

    def find_by_vkowners(self, index):
        result = self.vkowners.find_one(index, {'_id': 0})
        if result:
            return 0, result
        else:
            return 1, 'Not found.'

    def update_vkowners(self, index, data):
        coll.update(index, data)


if __name__ == '__main__':
    pass
