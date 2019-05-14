#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dbworker.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
from pymongo import MongoClient


connect = MongoClient()
db = connect.vkinder
vkinder = db.vkinder
vkusers = db.vkusers


def find_vkinder(user, login):
    """
    Метод производит поиск пользователя в БД. Если пользователь уже зарегистрирован в приложении,
    происходит заполнение атрибутов класса.
    """
    result = vkinder.find_one({'login': login})
    if result:
        user.id = result['id']
        user.first_name = result['first_name']
        user.last_name = result['last_name']
        user.screen_name = result['screen_name']
        user.interests = result['interests']
        user.music = result['music']
        user.movies = result['movies']
        user.books = result['books']
        user.token = result['token']
        user.login = result['login']
        user.city = result['city']
        user.groups = set(result['groups'])
        if 'age_min' in result:
            user.age_min = result['age_min']
            user.age_max = result['age_max']
            user.find_sex = result['find_sex']
            user.find_city = result['find_city']
            user.age_current = result['age_current']
            user.find_interests = result['find_interests']
        return 0, user.token
    else:
        return 1, 'Пользователь не найден.'


def update_user(user, login, data):
    """
    Метод производит обновление пользователя в таблице базы данных vkinder.
    """
    data.pop('is_closed', 0)
    data.pop('can_access_closed', 0)
    data['interests'] = data['interests'].split(',')
    data['login'] = login
    data['token'] = user.token
    vkinder.update({'login': login}, {'$set': data}, upsert=True)
    find_vkinder(user, login)


def update_find_params(user, data):
    """
    Метод обновляет параметры поиска в базе данных и в экземпляре класса.
    """
    data['age_current'] = user.age_current
    result = vkinder.update({'id': user.id}, {'$set': data}, upsert=False)
    find_vkinder(user, user.login)
    return result


def update_vkusers(user, data):
    vkinder.update({'id': user.id}, {'$set': {'age_current': user.age_current}}, upsert=False)
    for key, val in data.items():
        vkusers.update({'id': key}, val, upsert=True)


def search_vkuser(user_id):
    result = vkusers.find_one({'id': user_id})
    return result


def update_vkuser(user_id, data):
    result = vkusers.update({'id': user_id}, {'$set': data}, upsert=False)
    return result


if __name__ == '__main__':
    pass
