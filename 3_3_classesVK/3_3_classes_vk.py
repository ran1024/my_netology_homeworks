#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_2_classes.py
#

import requests
import functools
import pprint

TOKEN = 'b534eb8cb534eb8cb534eb8c80b55df025bb534b534eb8ce94b94b6299c2a63772794e9'


class GetUserVK:

    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id
        self.url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': self.access_token,
            'user_id': user_id,
            'fields': 'nickname',
            'v': 5.92,
        }


def get_user_vk(url, command, params):
    """
    Функция получает список друзей, удаляет забаненные и удалённые записи.
    Если получена команда friends: возвращается множество, содержащее
    идентификаторы друзей пользователя;
    Если получена команда users: возвращается список объектов пользователей.
    :param self:
    :return:
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


def main():
    users_id = (6888361, 23539, 8781042)
    url = 'https://api.vk.com/method/'
    params = {'access_token': TOKEN, 'fields': 'nickname', 'v': 5.92}

    mutual_friends_id = get_mutual_friend(url, users_id, params)
    if mutual_friends_id[0]:
        print("Число общих друзей:", len(mutual_friends_id))
        pprint.pprint(mutual_friends_id)
    else:
        print("У этих пользователей нет общих друзей!")
        exit(1)

    # mutual_friends = []
    params.pop('user_id')
    params.update({'fields': 'status, city, country, nickname', 'user_ids': ','.join(map(str, mutual_friends_id))})
    list_of_friends = get_user_vk(url, 'users', params)
    for i in range(len(list_of_friends)):
        pprint.pprint(list_of_friends[i])
        # mutual_friends.append(User(TOKEN, url, list_of_friends[i]))
    # pprint.pprint(list_of_friends)


main()

