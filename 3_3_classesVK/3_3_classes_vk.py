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
        params = self.get_params()
        params['user_id'] = user_id
        params['fields'] = ('nickname', 'city')
        response = requests.get('{0}users.get'.format(self.url), params)
        return response.json()


user1 = GetUserVK(TOKEN)
#user1_friends = user1.get_friends('6888361')
user1_friends = user1.get_friends('534652320')
pprint.pprint(user1_friends)

