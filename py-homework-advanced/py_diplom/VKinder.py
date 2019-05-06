#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import vk_api
from dbworker import UseDB


API_VERSION = '5.92'
APP_ID = 6888361
ACCESS_TOKEN = '9d5ac9e2eccc65f99f474bd99ed9d5cbdb7c413cbaaf43a96ec20b7677a947be915ab4450feec3d160a53'
# LOGIN = '+79241067661'
# PASSWORD = 'smallbitmap982'


# авторизация по токену или логин-паролю
def login_vk(token=None, login=None, password=None):
    try:
        if token:
            vk_session = vk_api.VkApi(token=token, app_id=APP_ID, api_version=API_VERSION)
        elif login and password:
            vk_session = vk_api.VkApi(login, password, api_version=API_VERSION,
                                      scope='friends,photos,audio,status,groups')
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
    text1 = '\nДля продолжения введите свой пароль в VK или Access Token, ' \
            'Рекомендуется получить Access Token. Для этого нужно перейти по ссылке:' \
            'https://oauth.vk.com/authorize?client_id=6888361&display=page' \
            '&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,audio,status,groups,offline' \
            '&response_type=token' \
            '\nАвторизоваться ВКонтакте и в открывшемся окне прочитать какие разрешения запрашивает ' \
            'это приложение, выдать приложению доступ, и из адресной строки следующего окна скопировать ' \
            'токен авторизации.\n'
    login = input('Введите номер телефона: ')
    my_db = UseDB()
    err, result = my_db.find_by_index('vkowners', {'login': login})
    if not err and result['token']:
        vk = login_vk(token=result['token'])
    else:
        print(text1)
        password = input('Введите токен или пароль: ')
        if len(password) > 50:
            vk = login_vk(token=password)
            err, result = my_db.update_record('vkowners', )
        else:
            vk = login_vk(login=login, password=password)

    account = vk.account.getProfileInfo()
    print(account)
    print('\n')
    vk_tools = vk_api.VkTools(vk)

    owner_data = vk.users.get(fields='interests, music, movies, books, screen_name')
    owner_data.pop('is_closed', 0)
    owner_data.pop('can_access_closed', 0)
    owner_data['token'] =
    print(owner_data)


if __name__ == '__main__':
    import sys
    sys.exit(main())
