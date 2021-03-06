#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# py-diplom.py
#
# Программа выводит список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
# Входные данные: имя пользователя или его id в ВК, для которого проводится исследование.
# Программа работает в терминальной сессии Linux.
#

import npyscreen
from time import sleep
import requests
import json


class UserVK:

    def __init__(self):
        self.url = 'https://api.vk.com/method/'
        self.token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
        self.user_id = ''
        self.user_name = ''
        self.user_friends = []
        self.user_groups = set()
        self.params = {
            'access_token': self.token,
            'fields': 'first_name',
            'v': 5.92,
        }

    def get_user_by_id(self, userid):
        """
        Функция получает ID пользователя.
        Возвращает имя пользователя или ошибку, если пользователя не существует.
        :param id:
        :return:
        """
        self.params['user_ids'] = userid
        response = requests.get('{0}users.get'.format(self.url), self.params)
        try:
            result = response.json()['response'][0]
            self.user_name = f"{result['first_name']} {result['last_name']}"
            self.user_id = userid
            return 'user_email', self.user_name
        except KeyError:
            return 'Error', 'Такого пользователя не существует! Для следующей попытки нажмите "Старт".'
        finally:
            del self.params['user_ids']

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
                return 'Error', 'Это не пользователь а группа или приложение. Для следующей попытки нажмите "Старт".'
        except TypeError:
            return 'Error', 'Такого пользователя не существует! Для следующей попытки нажмите "Старт".'
        finally:
            del self.params['screen_name']

    def get_friends(self, user_id=None):
        """
        Функция получает список друзей, удаляет забаненные и удалённые записи.
        Возвращает количество друзей пользователя. Список, содержащий id друзей
        пользователя запоминается в атрибуте экземпляра класса.
        :param user_id:
        :return:
        """
        if user_id is not None:
            self.user_id = user_id

        self.params['user_id'] = self.user_id
        response = requests.get('{0}friends.get'.format(self.url), self.params)
        try:
            friend_list = response.json()['response']['items']
            while friend_list:
                item = friend_list.pop()
                if 'deactivated' not in item:
                    self.user_friends.append(item['id'])
            return 'count', response.json()['response']['count']
        except KeyError:
            return 'Error', 'Не удалось получить список друзей. Для следующей попытки нажмите "Старт".'
        finally:
            del self.params['user_id']

    def get_groups(self, user_id=None):
        """
        Если не указан user_id, функция возвращает количество групп у пользователя,
        а множество, содержащее id групп пользователя запоминается в атрибуте экземпляра класса.
        Если указан user_id, возвращается множество с перечнем id групп пользователя.
        :param user_id:
        :return:
        """
        if user_id is None:
            self.params['user_id'] = self.user_id
        else:
            self.params['user_id'] = user_id
        response = requests.get('{0}groups.get'.format(self.url), self.params)
        try:
            result = response.json()['response']['items']
        except KeyError:
            return 'Error', 'Профиль пользователя закрыт или отключён! Для следующей попытки нажмите "Старт".'
        if user_id is None:
            self.user_groups = set(result)
            return 'count', response.json()['response']['count']
        else:
            return 'friend', set(result)

    def get_group_info(self, list_groups):
        """
        Получаем список групп и возвращаем массив словарей атрибутов этих групп.
        :param list_groups:
        :return:
        """
        self.params['group_ids'] = str(list_groups)
        self.params['fields'] = 'members_count'
        del self.params['user_id']
        out_list = []
        response = requests.get('{0}groups.getById'.format(self.url), self.params)
        try:
            result = response.json()['response']
            for item in result:
                var = {
                    'name': item['name'],
                    'gid': item['id'],
                    'members_count': item['members_count']
                }
                out_list.append(var)
            return 'groups', out_list
        except KeyError:
            return 'Error', 'Произошла ошибка при запросе параметров групп.'


class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Шпионские игры")


class InputBox(npyscreen.BoxTitle):
    # MultiLineEdit теперь будет окружен боксом
    _contained_widget = npyscreen.MultiLineEdit


class MainForm(npyscreen.ActionForm):
    # Конструктор
    def create(self):
        self.__class__.CANCEL_BUTTON_TEXT = 'Старт'
        self.__class__.CANCEL_BUTTON_BR_OFFSET = (2, 14)
        self.__class__.OK_BUTTON_TEXT = 'Выход'
        self.y, self.x = self.useable_space()
        self.user_name_id = self.add(npyscreen.TitleText,
                                     name="Имя пользователя или ID:",
                                     use_two_lines=False,
                                     begin_entry_at=25,
                                     value="",
                                     field_width=50)
        self.add(npyscreen.FixedText, value=''.join(['-' for i in range(self.x - 4)]), editable=False)
        self.text1 = self.add(npyscreen.FixedText, value='', editable=False)
        self.text2 = self.add(npyscreen.FixedText, value='', editable=False)
        self.text3 = self.add(npyscreen.FixedText, value='', editable=False)
        self.text4 = self.add(npyscreen.FixedText, value='', editable=False,
                              color='GOOD', rely=8, relx=self.x // 2 - 14)
        self.text5 = self.add(npyscreen.FixedText, value='', editable=False, color='CONTROL', rely=10)
        self.text6 = self.add(npyscreen.FixedText, value='', editable=False, color='DANGER', rely=11)

        self.box = self.add(InputBox, name="Результат", rely=13, height=self.y - 18,
                            color='STANDOUT', editable=False)

        self.slider = self.add(npyscreen.SliderPercent, out_of=100, step=0.01, rely=self.y - 4, editable=False)
        self.user = UserVK()
        self.ind = 0

    def get_diff_groups(self):
        """
        Вычисляем список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
        Получаем атрибутв каждой группы, выводим на экран и пишем в файл в виде json.
        :return:
        """
        secret_groups = self.user.user_groups
        # self.text5.value = f'Группы пользователя: {secret_groups}'
        self.widget_update()
        num = 0
        a = round(97 / len(self.user.user_friends), 2)

        for friend_id in self.user.user_friends:
            num += 1
            result = self.user.get_groups(friend_id)
            if result[0] == 'Error':
                self.text6.value = f'Друг № {num} id: {friend_id} недоступен и учитываться не будет.'
                continue
            if result[0] == 'friend':
                if result[1]:
                    secret_groups.difference_update(result[1])
                    self.text4.value = f'Друг № {num}  ID: {friend_id}'
                    self.text5.value = f'Группы: {secret_groups}'
            if self.slider.value + a <= 100:
                self.slider.value += a
            self.widget_update()
            sleep(0.1)

        self.text6.value = ''
        self.text4.value = f'Количество секретных групп: {len(secret_groups)}'
        self.text5.value = ''
        self.slider.value = 100
        secret_str = ','.join([str(q) for q in secret_groups])
        result = self.user.get_group_info(secret_str)
        if result[0] == 'Error':
            self.if_error(result[1])
        else:
            out_str = json.dumps(result[1], indent=1, ensure_ascii=False)
            self.box.value = out_str
            try:
                with open('groups.json', "w") as fh:
                    fh.write(out_str)
                self.text5.value = 'Результат записан в файл "groups.json".'
            except EnvironmentError as err:
                self.text6.value = 'Не удалось записать результат в файл "groups.json".'

    def processing_of_result(self, result, text):
        if result[0] == 'Error':
            self.if_error(result[1])
        else:
            self.text1.value = f'{text} пользователя: {result[1]}'
            self.slider.value = 1
            self.widget_update()
            result = self.user.get_friends()
            if result[0] == 'Error':
                self.if_error(result[1])
            else:
                self.text2.value = f'Количество друзей: {result[1]}'
                self.slider.value = 2
                self.widget_update()
                if not result[1]:
                    self.if_error('У пользователя нет друзей. Для следующей попытки нажмите "Старт".')
                    return
                self.ind = 1
                result = self.user.get_groups()
                if result[0] == 'Error':
                    self.if_error(result[1])
                else:
                    self.text3.value = f'Количество групп: {result[1]}'
                    self.slider.value = 3
                    self.widget_update()
                    self.ind = 1
                    if not result[1]:
                        self.if_error('Пользователь не состоит ни в одной группе!'
                                      ' Для следующей попытки нажмите "Старт".')
                        return
                    self.get_diff_groups()

    def get_user_attr(self):
        self.user_name_id.editable = False
        if self.user_name_id.value.isdigit():
            result = self.user.get_user_by_id(self.user_name_id.value)
            self.processing_of_result(result, 'Имя')
        else:
            result = self.user.get_userid_by_name(self.user_name_id.value)
            self.processing_of_result(result, 'ID')

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
            self.text3.value = ''
            self.text4.value = ''
            self.text5.value = ''
            self.text6.value = ''
            self.slider.value = 0

    def widget_update(self):
        self.text1.display()
        self.text2.display()
        self.text3.display()
        self.text4.display()
        self.text5.display()
        self.text6.display()
        self.slider.display()

    def if_error(self, msg):
        self.user_name_id.value = ''
        self.slider.value = 100
        self.text6.value = msg
        self.ind = 0


if __name__ == '__main__':
    MyApp = App()
    MyApp.run()
