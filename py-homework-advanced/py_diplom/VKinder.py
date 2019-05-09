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
        print(f'Произошла ошибка авторизации: {result[1]}.\n Попробуйте ещё раз.')
        return 1
    else:
        return 0


def get_find_params(vkinder, vk_connect):
    """
    Получаем от пользователя необходимые параметры для поиска.
    """
    print('Для поиска необходимо ввести несколько параметров.')
    try:
        age_min = int(input('Введите минимальный возраст поиска: '))
        age_max = int(input('Введите максимальный возраст поиска: '))
        sex_variant = {'м': 2, 'ж': 1}
        sex = input('Введите пол ("М". "Ж"): ').lower()
        sex = sex_variant[sex]
    except (ValueError, KeyError):
        return 1

    city_title = input('Введите город для поиска: ')
    if city_title:
        result = vk_connect.vk.database.getCities(country_id=1, q=city_title, need_all=0, count=1)
        # Если был введён некорректный населённый пункт:
        if not result['count']:
            return 1
        find_city = result['items'][0]
    else:
        find_city = vkinder.city
    interests = input('Введите желаемые интересы через запятую: ').split(',')

    find_data = {'age_min': age_min, 'age_max': age_max, 'find_sex': sex,
                 'find_city': find_city, 'find_interests': interests}
    vkinder.update_find_params(find_data)
    return 0


def user_login(vkinder, vk_connect):
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
            res = vk_connect.login_vk(token=result[1])
            session_ok = if_error(res)
        else:
            print(text1)
            password = input('Введите токен или пароль: ')
            if len(password) > 50:
                vkinder.token = password
                res = vk_connect.login_vk(token=password)
            else:
                res = vk_connect.login_vk(login=login, password=password)
            session_ok = if_error(res)
        if not session_ok:
            vkinder.update_user(login, vk_connect.vk)


def users_search(vkinder, vk_connect, offset):
    fields = 'relation, photo_max_orig, is_friend, common_count, occupation, interests, music, movies, books'
    relation = {0: 'не указано',
                1: 'в браке не состоит',
                2: 'есть друг или подруга',
                3: 'помолвлен / помолвлена',
                4: 'состоит в браке',
                5: 'всё сложно',
                6: 'в активном поиске',
                7: 'влюблён / влюблена',
                8: 'в гражданском браке'}
    users = []
    result = vk_connect.vk.users.search(offset=offset, count=10, city=vkinder.find_city['id'],
                                        country=1, sex=vkinder.find_sex, age_from=vkinder.age_min,
                                        age_to=vkinder.age_max, has_photo=1, fields=fields)
    if not result['count']:
        return users

    for item in result['items']:
        item_dict = {'Реципиент': f'{item["first_name"]} {item["last_name"]}',
                     'Фотография': item['photo_max_orig']}
        if 'relation' in item and item['relation'] in [0, 1, 2, 5, 6, 7]:
            item_dict['Семейное положение'] = relation[item['relation']]
        else:
            item_dict['Семейное положение'] = 'не указано'
        if 'occupation' in item:
            if item['occupation']['type'] == 'university':
                item_dict['Образование'] = f'высшее: {item["occupation"]["name"]}'
            elif item['occupation']['type'] == 'work':
                item_dict['Работает в'] = item['occupation']['name']
            elif item['occupation']['type'] == 'school':
                item_dict['Образование'] = f'школа: {item["occupation"]["name"]}'
        item_dict['Является ли Вашим другом'] = 'да' if item['is_friend'] else 'нет'
        item_dict['Количество общих друзей'] = item['common_count']
        users.append(item_dict)
    return users


def main():
    connect = MongoClient()
    db = connect.vkinder
    vkinder = Vkinder(db)
    vk_connect = VkSession()
    user_login(vkinder, vk_connect)
    result = 1
    while result:
        result = get_find_params(vkinder,vk_connect)
        if result:
            print('\nБыли введены неправильные параметры! Попробуйте ещё раз.\n')

    print('\nЭто класс Vkinder:\n', vkinder)

    print(f'\nОсуществляется поиск. Параметры:\nГод рождения: {vkinder.age_current}\n'
          f'Пол: {vkinder.find_sex} (1-женский, 2-мужской)\n'
          f'Город: {vkinder.find_city["title"]}\nИнтересы: {vkinder.find_interests}\n')
    offset = 0
    users = users_search(vkinder, vk_connect, offset)
    print(users, '\n')
    if users:
        for user in users:
            for key, val in user.items():
                print(f'{key}: {val}')
            print('\n')
    # account = vk.account.getProfileInfo()
    # vk_tools = vk_api.VkTools(vk)
    # print(my_db.vkowners.find_one({'login': login}, {'_id': 0}))


if __name__ == '__main__':
    import sys
    sys.exit(main())
