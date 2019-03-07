#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_2_classes.py
#

import requests
import pprint

TOKEN = 'b534eb8cb534eb8cb534eb8c80b55df025bb534b534eb8ce94b94b6299c2a63772794e9'

class GetUserVK:

    def __init__(self, access_token):
        self.access_token = access_token
        self.url = 'https://api.vk.com/method/'

    def get_params(self):
        return {
            'access_token': self.access_token,
            'v': 5.92,
        }

    def get_friends(self, user_id):
        """
        Функция получает список друзей, удаляет забаненные и удалённые записи.
        Возвращает список славарей: {идентификатор: имя_фамилия} друзей пользователя.
        :param user_id:
        :return:
        """
        params = self.get_params()
        params['user_id'] = user_id
        params['fields'] = 'nickname'
        response = requests.get('{0}friends.get'.format(self.url), params)
        friend_list = response.json()['response']['items']
        friends = []
        while friend_list:
            item = friend_list.pop()
            if 'deactivated' not in item:
               friends.append({item['id']: item['first_name'] + ' ' + item['last_name']})
        return friends


user1 = GetUserVK(TOKEN)
user1_friends = user1.get_friends('6888361')
user2 = GetUserVK(TOKEN)
user2_friends = user1.get_friends('23539')

#user1_friends = user1.get_friends('1945830')
print(len(user1_friends))
pprint.pprint(user1_friends)

