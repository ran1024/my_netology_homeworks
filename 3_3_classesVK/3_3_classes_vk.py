#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_2_classes.py
#

import requests
import functools
import pprint

TOKEN = 'b534eb8cb534eb8cb534eb8c80b55df025bb534b534eb8ce94b94b6299c2a63772794e9'


class UserVK:
    """
    Класс, описывающий пользователя ВК.
    Команда print(user) выводит ссылку на профиль пользователя в сети VK.
    """
    def __init__(self, url, params, user_dict):
        self.url = url
        self.user_dict = user_dict
        self.params = params

    def __str__(self):
        return "https://vk.com/id{}".format(self.get_user_id())

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


def get_user_vk(url, command, params):
    """
    Функция получает список друзей, удаляет забаненные и удалённые записи.
    Если получена команда friends: возвращается множество, содержащее
    идентификаторы друзей пользователя;
    Если получена команда users: возвращается список объектов пользователей.
    """
    response = requests.get('{0}{1}.get'.format(url, command), params)
    if command == 'friends':
        friend_list = response.json()['response']['items']
        friends = set()
        while friend_list:
            item = friend_list.pop()
            if 'deactivated' not in item:
                friends.add(item['id'])
        return friends
    else:
        return response.json()['response']


def get_mutual_friend(url, users_id, params):
    """
    Функция принимает произвольное количество id пользователей и возвращает
    список id общих друзей.
    :param url:
    :param users_id:
    :param params:
    :return:
    """
    users_friend = []
    for i in range(len(users_id)):
        params['user_id'] = users_id[i]
        users_friend.append(get_user_vk(url, 'friends', params))
        print(f"User {users_id[i]} имеет {len(users_friend[i])} друзей.")

    return list(functools.reduce(lambda x, y: x & y, users_friend))


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
        print('{0:10} {1}\n'.format('Country:', friend.get_user_country()))


def main():
    users_id = (6888361, 23539, 8781042)
    url = 'https://api.vk.com/method/'
    params = {'access_token': TOKEN, 'fields': 'nickname', 'v': 5.92}

    mutual_friends_id = get_mutual_friend(url, users_id, params)
    if mutual_friends_id:
        print("Число общих друзей:", len(mutual_friends_id))
        pprint.pprint(mutual_friends_id)
    else:
        print("У этих пользователей нет общих друзей!")
        exit(1)

    mutual_friends = []
    params.pop('user_id')
    params.update({'fields': 'status, city, country, nickname', 'user_ids': ','.join(map(str, mutual_friends_id))})
    list_of_friends = get_user_vk(url, 'users', params)
    for friend in list_of_friends:
        mutual_friends.append(UserVK(url, params, friend))

    for friend in mutual_friends:
        print(friend)


main()

