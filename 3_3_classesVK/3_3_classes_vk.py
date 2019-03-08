#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_2_classes.py
#

import requests
import functools
import pprint


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
    Возвращает множество, содержащее идентификаторы друзей пользователя.
    :param self:
    :return:
    """
    response = requests.get('{0}{1}.get'.format(url, command), params)
    friend_list = response.json()['response']['items']
    friends = set()
    while friend_list:
        item = friend_list.pop()
        if 'deactivated' not in item:
            friends.add(item['id'])
    return friends


def main():
    users_id = (6888361, 23539, 8781042)
    url = 'https://api.vk.com/method/'
    TOKEN = 'b534eb8cb534eb8cb534eb8c80b55df025bb534b534eb8ce94b94b6299c2a63772794e9'
    users_friend = []
    params = {'access_token': TOKEN, 'fields': 'nickname', 'v': 5.92}

    for i in range(len(users_id)):
        params['user_id'] = users_id[i]
        users_friend.append(get_user_vk(url, 'friends', params))
        print(f"User {users_id[i]} имеет {len(users_friend[i])} друзей.")

    friends_id = list(functools.reduce(lambda x, y: x & y, users_friend))
    if friends_id[0]:
        print("Число общих друзей:", len(friends_id))
        pprint.pprint(friends_id)
    else:
        print("У этих пользователей нет общих друзей!")
        exit(1)


main()

