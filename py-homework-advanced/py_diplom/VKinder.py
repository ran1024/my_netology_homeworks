#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import vk_api

API_VERSION = '5.92'
APP_ID = 6888361
ACCESS_TOKEN = '86c616ef76bc5b3ac9f7018c5203483499ebcbc5e6ee9b81dc1de27b2938f1ba63c9af27853353cbfda02'
LOGIN = '+79241067661'
PASSWORD = 'smallbitmap982'


# авторизация по токену или логин-паролю
def login_vk(token=None, login=None, password=None):
    try:
        if token:
            vk_session = vk_api.VkApi(token=token, app_id=APP_ID, api_version=API_VERSION)
        elif login and password:
            vk_session = vk_api.VkApi(login, password, api_version=API_VERSION,
                                      scope='friends,photos,audio,status,groups,messages')
            vk_session.auth(token_only=True, reauth=True)
        else:
            raise KeyError('Не введен токен или логин-пароль')
        return vk_session.get_api()
    except Exception as e:
        print(e)


def get_albums(vk, vk_tools):
    albums = []
    for album in vk.photos.getAlbums(need_system=1)['items']:
        # получаем список фотографий из альбома
        photos = vk_tools.get_all(values={'album_id': album['id'], 'photo_sizes': 1}, method='photos.get', max_count=3)
        # добавляем название альбома и ссылки на каждую фотографию
        albums.append({'name': album['title'], 'photos': [p['sizes'][-1]['url'] for p in photos['items']]})
    print(albums)


def main():
    # vk = login_vk(login=LOGIN, password=PASSWORD)
    vk = login_vk(ACCESS_TOKEN)
    account = vk.account.getProfileInfo()
    print(account)
    print('\n')
    vk_tools = vk_api.VkTools(vk)

    owner_data = vk.users.get(fields='interests, music, movies, books, screen_name')
    print(owner_data)


if __name__ == '__main__':
    import sys
    sys.exit(main())
