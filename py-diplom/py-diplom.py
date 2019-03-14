#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# py-diplom.py
#

import npyscreen
from time import sleep
import requests

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
url = 'https://api.vk.com/method/'


class UserVK:

    def __init__(self):
        self.url = 'https://api.vk.com/method/'
        self.token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
        self.user_id = ''
        self.user_friends = []
        self.params = {
            'access_token': self.token,
            'v': 5.92,
        }

    def get_userid_by_name(self, name):
        """
        # Функция находит ID пользователя по его имени.
        :param name:
        :return:
        """
        self.params['screen_name'] = name
        response = requests.get('{0}utils.resolveScreenName'.format(self.url), self.params)
        try:
            result = response.json()['response']
            if result['type'] == 'user':
                self.user_id = result["object_id"]
                return 'id', self.user_id
            else:
                return 'Error', 'Это не пользователь а группа или приложение.'
        except TypeError:
            return 'Error', 'Такого пользователя не существует! Для следующей попытки нажмите "Старт".'
        finally:
            del self.params['screen_name']


    def get_friends(self, user_id=None):
        """
        Функция получает список друзей, удаляет забаненные и удалённые записи.
        Возвращает множество, содержащее имена и фамилии друзей пользователя.
        :return:
        """
        if user_id is not None:
            self.user_id = user_id

        self.params['user_id'] = self.user_id
        self.params['fields'] = 'first_name'
        response = requests.get('{0}friends.get'.format(self.url), self.params)
        try:
            friend_list = response.json()['response']['items']
            while friend_list:
                item = friend_list.pop()
                if 'deactivated' not in item:
                    self.user_friends.append(str(item['id']))
            return 'count', response.json()['response']['count']
        except KeyError:
            return 'Error', 'Не удалось получить список друзей. Для следующей попытки нажмите "Старт".'


class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Шпионские игры")


class MainForm(npyscreen.ActionForm):
    # Конструктор
    def create(self):
        self.__class__.CANCEL_BUTTON_TEXT = 'Старт'
        self.__class__.CANCEL_BUTTON_BR_OFFSET = (2, 14)
        self.__class__.OK_BUTTON_TEXT = 'Выход'
        self.y, self.x = self.useable_space()
        self.user_name_id = self.add(npyscreen.TitleText,
                                     name="Имя ползователя или ID:",
                                     use_two_lines=False,
                                     begin_entry_at=24,
                                     value="",
                                     field_width=50)
        self.add(npyscreen.FixedText, value=''.join(['-' for i in range(self.x - 4)]), editable=False)
        self.text1 = self.add(npyscreen.FixedText, value='', editable=False)
        self.text2 = self.add(npyscreen.FixedText, value='', editable=False)

        self.slider = self.add(npyscreen.SliderPercent, out_of=100, step=1, rely=self.y - 4, editable=False)
        self.ind = 0

    def get_user_attr(self):
        user = UserVK()
        self.user_name_id.editable = False
        if self.user_name_id.value.isdigit():
            result = user.get_friends(self.user_name_id.value)
            if result[0] == 'Error':
                self.user_name_id.value = ''
                self.text2.value = result[1]
            else:
                self.text2.value = f'Количество друзей: {result[1]}'
                self.slider.value = 10
                self.ind = 1
        else:
            result = user.get_userid_by_name(self.user_name_id.value)
            if result[0] == 'Error':
                self.user_name_id.value = ''
                self.text1.value = result[1]
            elif result[0] == 'id':
                self.text1.value = f'ID пользователя: {result[1]}'
                self.slider.value = 5
                result = user.get_friends()
                if result[0] == 'Error':
                    self.text2.value = result[1]
                    self.user_name_id.value = ''
                else:
                    self.text2.value = f'Количество друзей: {result[1]}'
                    self.slider.value = 10
                    self.ind = 1

    # переопределенный метод, срабатывающий при нажатии на кнопку «Выход»
    def on_ok(self):
        exit(0)

    # переопределенный метод, срабатывающий при нажатии на кнопку «Старт»
    def on_cancel(self):
        if self.ind:
            return
        if self.user_name_id.value:
            self.get_user_attr()
        else:
            self.user_name_id.editable = True
            self.text1.value = ''
            self.text2.value = ''


if __name__ == '__main__':
    MyApp = App()
    MyApp.run()
    # main()
