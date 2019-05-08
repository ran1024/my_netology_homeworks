#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dbworker.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
from datetime import datetime


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
        self.find_city = {}
        self.age_current = 0
        self.find_interests = []
        self.token = ''
        self.login = ''
        self.city = {}

    def __str__(self):
        return f'{{\n\tid: {self.id},\n\tfirst_name: {self.first_name}\n\tlast_name: {self.last_name}\n\t' \
            f'screen_name: {self.screen_name}\n\tlogin: {self.login}\n\tcity: {self.city}\n\t' \
            f'interests: {self.interests}\n\tmusic: {self.music}\n\tmovies: {self.movies}\n\t' \
            f'books: {self.books}\n\ttoken: {self.token}\n\tage_min: {self.age_min}\n\t' \
            f'age_max: {self.age_max}\n\tage_current: {self.age_current}\n\tfind_sex: {self.find_sex}\n\t' \
            f'find_city: {self.find_city}\n\tfind_interests: {self.find_interests}\n }}'

    def find_vkinder(self, login):
        """
        Метод производит поиск пользователя в БД. Если пользователь уже зарегистрирован в приложении,
        произходит заполнение атрибутов класса.
        """
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
            self.token = result['token']
            self.login = result['login']
            self.city = result['city']
            if 'age_min' in result:
                self.age_min = result['age_min']
                self.age_max = result['age_max']
                self.find_sex = result['find_sex']
                self.find_city = result['find_city']
                self.age_current = result['age_current']
                self.find_interests = result['find_interests']
            return 0, self.token
        else:
            return 1, 'Пользователь не найден.'

    def update_user(self, login, vk):
        """
        Метод запрашивает данные пользователя в ВК (т.к. они могли измениться с момента
        предыдущего запуска) и производит обновление записи в таблице базы данных vkinder.
        """
        result = vk.users.get(fields='interests, music, movies, books, screen_name, city')
        user = result[0]
        user['interests'] = user['interests'].split(',')
        user.pop('is_closed', 0)
        user.pop('can_access_closed', 0)
        user['login'] = login
        user['token'] = self.token
        self.vkinder.update({'login': login}, {'$set': user}, upsert=True)
        self.find_vkinder(login)

    def update_find_params(self, data):
        """
        Метод обновляет параметры поиска в базе данных и в экземпляре класса.
        """
        data['age_current'] = self.age_current
        result = self.vkinder.update({'id': self.id}, {'$set': data}, upsert=False)
        self.find_vkinder(self.login)
        return result


if __name__ == '__main__':
    pass
