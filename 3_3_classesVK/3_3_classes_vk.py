#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 3_3_classes_vk.py
#
# Программа принимает произвольное количество id пользователей и возвращает
# число и список общих друзей в виде массива экземпляров классов. Забаненные
# и удалённые записи друзей не учитываются. Команда print(user) выводит ссылку
# на профиль пользователя в сети VK.
# В качестве токена использовался мой сервисный ключ.
#

import requests
import functools

TOKEN = 'b534eb8cb534eb8cb534eb8c80b55df025bb534b534eb8ce94b94b6299c2a63772794e09'


class UserVK:
    """
    Класс, описывающий пользователя ВК.
    Команда print(user) выводит ссылку на профиль пользователя в сети VK.
    """
    def __init__(self, user_dict):
        self.user_dict = user_dict

    def __str__(self):
        return "https://vk.com/id{}".format(self.get_user_id())

    def __and__(self, other):
        return self.user_dict['friends'] & other.user_dict['friends']

    def get_user_id(self):
        return self.user_dict['id']

    def get_user_name(self):
        return f"{self.user_dict['first_name']} {self.user_dict['last_name']}"

    def get_user_nickname(self):
        return self.user_dict['nickname'] if self.user_dict['nickname'] else 'Nickname не указан.'

    def get_user_status(self):
        return self.user_dict['status'] if self.user_dict['status'] else 'Статус не указан'

    def get_user_city(self):
        return self.user_dict['city']['title'] if 'city' in self.user_dict else 'Город не указан.'

    def get_user_country(self):
        return self.user_dict['country']['title'] if 'country' in self.user_dict else 'Страна не указана.'

    def get_user_friends(self):
        return self.user_dict['friends'] if self.user_dict['friends'] else 'Список друзей пуст.'


def get_users_vk(url, params):
    """
    Функция получает список пользователей, удаляет забаненные и удалённые записи.
    Возвращает список объектов пользователей, в которые вставлено множество c ключём
    'friends', содержащее идентификаторы друзей пользователя;
    :param url:
    :param params:
    :return:
    """
    users_vk = []
    try:
        response1 = requests.get('{0}users.get'.format(url), params)
        params.pop('user_ids')
        for user in response1.json()['response']:
            friends = set()
            params['user_id'] = user['id']
            response2 = requests.get('{0}friends.get'.format(url), params)
            for item in response2.json()['response']['items']:
                if 'deactivated' not in item:
                    friends.add(item['id'])
            user['friends'] = friends
            users_vk.append(user)
        return users_vk
    except KeyError:
        print('Произошла ошибка при получении запроса:', response1.json())
        exit(1)
    except requests.exceptions.RequestException as err:
        print('Requests error:', err)


def test(mutual_friends):
    """
    Тест работы методов объекта пользователя.
    :param mutual_friends:
    :return:
    """
    for friend in mutual_friends:
        print('{0:10} {1}'.format('ID:', friend.get_user_id()))
        print('{0:10} {1}'.format('Имя:', friend.get_user_name()))
        print('{0:10} {1}'.format('Nickname:', friend.get_user_nickname()))
        print('{0:10} {1}'.format('Status:', friend.get_user_status()))
        print('{0:10} {1}'.format('City:', friend.get_user_city()))
        print('{0:10} {1}'.format('Country:', friend.get_user_country()))
        print('{0:10} {1}\n'.format('friends:', friend.get_user_friends()))


def main():
    users_id = (6888361, 23539, 8781042)
    url = 'https://api.vk.com/method/'
    params = {'access_token': TOKEN,
              'fields': 'status, city, country, nickname',
              'v': 5.92,
              'user_ids': ','.join(map(str, users_id))}

    mutual_friends = []
    users_list = []
    for user_dict in get_users_vk(url, params):
        users_list.append(UserVK(user_dict))

    users_friends = []
    try:
        for i in range(len(users_list)):
            users_friends.append(users_list[i] & users_list[i+1])
    except IndexError:
        mutual_friends_id = list(functools.reduce(lambda x, y: x & y, users_friends))
        if mutual_friends_id:
            print("Число общих друзей:", len(mutual_friends_id))
            params.pop('user_id')
            params.update({'user_ids': ','.join(map(str, mutual_friends_id))})
            for user_dict in get_users_vk(url, params):
                mutual_friends.append(UserVK(user_dict))
        else:
            print("У этих пользователей нет общих друзей!")
            exit(1)

    for friend in mutual_friends:
        print(friend)

    # test(mutual_friends)

main()

