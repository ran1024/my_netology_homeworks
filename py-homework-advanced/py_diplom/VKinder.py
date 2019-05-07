#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import vk_api
from pymongo import MongoClient
from dbworker import Vkinder


class VkSession:

    API_VERSION = '5.92'
    APP_ID = 6888361

    def __init__(self):
        self.vk_session = None
        self.vk = None
        self.vk_tools = None

    def login_vk(self, token=None, login=None, password=None):
        """
        Авторизация по токену или логин-паролю.
        """
        try:
            if token:
                self.vk_session = vk_api.VkApi(token=token, app_id=VkSession.APP_ID,
                                               api_version=VkSession.API_VERSION)
            elif login and password:
                self.vk_session = vk_api.VkApi(login, password, api_version=VkSession.API_VERSION,
                                               scope='friends,photos,audio,status,groups')
                self.vk_session.auth(token_only=True, reauth=True)
            else:
                raise KeyError('Не введен токен или логин-пароль')
            self.vk = self.vk_session.get_api()
            self.vk_tools = vk_api.VkTools(self.vk_session)
            return 0, 'ok'
        except Exception as error_msg:
            return 1, f'Ошибка: {error_msg}'

    def get_albums(self):
        albums = []
        for album in self.vk.photos.getAlbums(need_system=1)['items']:
            # получаем список фотографий из альбома
            photos = self.vk_tools.get_all(values={'album_id': album['id'], 'photo_sizes': 1},
                                           method='photos.get', max_count=3)
            # добавляем название альбома и ссылки на каждую фотографию
            albums.append({'name': album['title'], 'photos': [p['sizes'][-1]['url'] for p in photos['items']]})
        return albums


def if_error(result):
    if result[0]:
        print('Произошла ошибка авторизации. Попробуйте ещё раз.')
        print(result[1])
        return 1
    else:
        return 0


def get_find_param():
    print('Для поиска необходимо ввести несколько параметров.')
    age_from = input('Введите минимальный возраст поиска: ')
    age_to = input('Введите максимальный возраст поиска: ')
    sex = input('Введите пол ("М". "Ж"): ')
    sex = '1' if sex == 'М' else '2'
    find_city = input('Введите город для поиска: ')
    return [age_from, age_to, sex, find_city]


def main():
    connect = MongoClient()
    db = connect.vkinder
    vkinder = Vkinder(db)
    vk_session = VkSession()
    text1 = '\nДля продолжения введите свой пароль в VK или Access Token, ' \
            'Рекомендуется получить Access Token. Для этого нужно перейти по ссылке:' \
            'https://oauth.vk.com/authorize?client_id=6888361&display=page' \
            '&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,audio,status,groups,offline' \
            '&response_type=token' \
            '\nАвторизоваться ВКонтакте и в открывшемся окне прочитать какие разрешения запрашивает ' \
            'это приложение, выдать приложению доступ, и из адресной строки следующего окна скопировать ' \
            'токен авторизации.\n'
    session_ok = 1
    while session_ok:
        login = input('Введите номер телефона: ')
        result = vkinder.find_vkinder(login)
        if not result[0] and result[1]:
            res = vk_session.login_vk(token=result[1])
            session_ok = if_error(res)
        else:
            print(text1)
            password = input('Введите токен или пароль: ')
            if len(password) > 50:
                vkinder.token = password
                res = vk_session.login_vk(token=password)
            else:
                res = vk_session.login_vk(login=login, password=password)
            session_ok = if_error(res)
        if not session_ok:
            vkinder.update_user(login, vk_session.vk)
            print('Это класс Vkinder:\n', vkinder)

    # account = vk.account.getProfileInfo()
    # vk_tools = vk_api.VkTools(vk)
    # print(my_db.vkowners.find_one({'login': login}, {'_id': 0}))


if __name__ == '__main__':
    import sys
    sys.exit(main())
