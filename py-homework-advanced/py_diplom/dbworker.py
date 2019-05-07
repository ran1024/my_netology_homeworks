#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dbworker.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
from datetime import datetime


# class UseDB:
#     """
#     Здесь собраны все средства для работы с базой данных.
#     """
#     def __init__(self):
#         self.client = MongoClient()
#         self.db = self.client.vkinder
#         self.vkowners = self.db.vkowners
#         self.vkusers = self.db.vkusers
#
#     def find_by_vkowners(self, index):
#         result = self.vkowners.find_one(index, {'_id': 0})
#         if result:
#             return 0, result
#         else:
#             return 1, 'Not found.'
#
#     def update_vkowners(self, index, data):
#         coll.update(index, data)


class Vkinder:

    def __init__(self, db):
        self.vkinder = db.vkinder
        self.id = ''
        self.first_name = ''
        self.last_name = ''
        self.screen_name = ''
        self.interests = []
        self.music = []
        self.movies = []
        self.books = []
        self.age_min = 0
        self.age_max = 0
        self.find_sex = ''
        self.find_city = ''
        self.age_current = 0
        self.find_interests = []
        self.token = ''

    def __str__(self):
        return f'{{\n\tid: {self.id},\n\tfirst_name: {self.first_name}\n\tlast_name: {self.last_name}\n\t' \
            f'screen_name: {self.screen_name}\n\tinterests: {self.interests}\n\tmusic: {self.music}\n\t' \
            f'movies: {self.movies}\n\tbooks: {self.books}\n\tage_min: {self.age_min}\n\t' \
            f'age_max: {self.age_max}\n\tage_current: {self.age_current}\n\tfind_sex: {self.find_sex}\n\t' \
            f'find_city: {self.find_city}\n\tfind_interests: {self.find_interests}\n\ttoken: {self.token}\n }}'

    def find_vkinder(self, login):
        result = self.vkinder.find_one({'login': login})
        if result:
            self.id = result['id']
            self.first_name = result['first_name']
            self.last_name = result['last_name']
            self.screen_name = result['screen_name']
            self.interests = result['interests']
            self.music = result['music']
            self.movies = result['movies']
            self.books = result['books']
            self.age_min = result['age_min']
            self.age_max = result['age_max']
            self.find_sex = result['find_sex']
            self.find_city = result['find_city']
            self.age_current = result['age_current']
            self.find_interests = result['find_interests']
            self.token = result['token']
            return 0, self.token
        else:
            return 1, 'Пользователь не найден.'

    def update_user(self, login, vk):
        result = vk.users.get(fields='interests, music, movies, books, screen_name')
        user = result[0]
        user.pop('is_closed', 0)
        user.pop('can_access_closed', 0)
        user['login'] = login
        user['age_min'] = 0
        user['age_max'] = 0
        user['find_sex'] = ''
        user['find_city'] = ''
        user['age_current'] = 0
        user['find_interests'] = []
        user['token'] = self.token
        self.vkinder.update({'login': login}, user, upsert=True)
        self.find_vkinder(login)


if __name__ == '__main__':
    pass
