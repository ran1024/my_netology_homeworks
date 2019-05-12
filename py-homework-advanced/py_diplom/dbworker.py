#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dbworker.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#


class Vkinder:

    def __init__(self, db):
        self.vkinder = db.vkinder
        self.vkusers = db.vkusers
        self.id = ''
        self.first_name = ''
        self.last_name = ''
        self.screen_name = ''
        self.interests = []
        self.music = []
        self.movies = []
        self.books = []
        self.groups = set()
        self.age_min = 0
        self.age_max = 0
        self.find_sex = ''
        self.find_city = {}
        self.age_current = [1, 1]
        self.find_interests = []
        self.token = ''
        self.login = ''
        self.city = {}
        # self.offset = 0

    def __str__(self):
        return f' {{\n\tid: {self.id},\n\tfirst_name: {self.first_name}\n\tlast_name: {self.last_name}\n\t' \
            f'screen_name: {self.screen_name}\n\tlogin: {self.login}\n\tcity: {self.city}\n\t' \
            f'interests: {self.interests}\n\tmusic: {self.music}\n\tmovies: {self.movies}\n\t' \
            f'books: {self.books}\n\tgroups: {self.groups}\n\ttoken: {self.token}\n\t' \
            f'age_min: {self.age_min}\n\tage_max: {self.age_max}\n\tage_current: {self.age_current}\n\t' \
            f'find_sex: {self.find_sex}\n\tfind_city: {self.find_city}\n\t' \
            f'find_interests: {self.find_interests}\n }}'

    def find_vkinder(self, login):
        """
        Метод производит поиск пользователя в БД. Если пользователь уже зарегистрирован в приложении,
        происходит заполнение атрибутов класса.
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
            self.groups = set(result['groups'])
            if 'age_min' in result:
                self.age_min = result['age_min']
                self.age_max = result['age_max']
                self.find_sex = result['find_sex']
                self.find_city = result['find_city']
                self.age_current = result['age_current']
                self.find_interests = result['find_interests']
                # self.offset = result['offset']
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
        result = vk.groups.get(user_id=user['id'])
        user['groups'] = result['items']
        self.vkinder.update({'login': login}, {'$set': user}, upsert=True)
        self.find_vkinder(login)

    def update_find_params(self, data):
        """
        Метод обновляет параметры поиска в базе данных и в экземпляре класса.
        """
        data['age_current'] = self.age_current
        data['offset'] = 0
        result = self.vkinder.update({'id': self.id}, {'$set': data}, upsert=False)
        self.find_vkinder(self.login)
        return result

    def update_vkusers(self, data):
        self.vkinder.update({'id': self.id}, {'$set': {'age_current': self.age_current}}, upsert=False)
        for key, val in data.items():
            self.vkusers.update({'id': key}, val, upsert=True)

    def search_vkuser(self, user_id):
        result = self.vkusers.find_one({'id': user_id})
        return result

    def update_vkuser(self, user_id, data):
        result = self.vkusers.update({'id': user_id}, {'$set': data}, upsert=False)
        return result


if __name__ == '__main__':
    pass
