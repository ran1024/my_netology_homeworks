#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# vksession.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import vk_api


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

    def get_albums(self, user_id):
        """
        Получаем фотографии из всех альбомов для заданного реципиента, сортируем по рейтингу
        и выводим по топ-3 фото из каждого альбома.
        """
        albums = []
        for album in self.vk.photos.getAlbums(owner_id=user_id, need_system=1)['items']:
            # получаем список фотографий из альбома
            photos = self.vk_tools.get_all(values={'owner_id': user_id, 'album_id': album['id'],
                                                   'photo_sizes': 1, 'extended': 1},
                                           method='photos.get', max_count=3)
            # добавляем название альбома и ссылки на каждую фотографию
            a1 = [(p['sizes'][-1]['url'], p["likes"]["count"]) for p in photos['items']]
            albums.append(sorted(a1, key=lambda x: x[1], reverse=True)[:3])
        return albums

    def get_user_data(self):
        """
        Метод запрашивает данные пользователя в ВК включая группы.
        """
        result = self.vk.users.get(fields='interests, music, movies, books, screen_name, city')
        data = result[0]
        groups = self.vk.groups.get(user_id=data['id'])
        data['groups'] = groups['items']
        return data

    def find_city(self, city_title):
        """
        Ищем id города по названию. Возвращаем словарь {'id': id_города, 'title': название_города}.
        """
        result = self.vk.database.getCities(country_id=1, q=city_title, need_all=0, count=1)
        # Если был введён некорректный населённый пункт:
        if not result['count']:
            return 1, 'City not found.'
        return 0, result['items'][0]

    def find_users(self, vkinder):
        """
        С помощью API execute получаем всех пользователей по данным параметрам.
        """
        fields = 'relation, photo_max_orig, is_friend, common_count, occupation, interests, music, movies, books'
        result, errors = vk_api.vk_request_one_param_pool(
            self.vk_session,
            'users.search',  # Метод
            key='status',    # Изменяющийся параметр
            values=[1, 2, 5, 6],
            default_values={
                'count': 1000,
                'city': vkinder.find_city['id'],
                'country': 1,
                'sex': vkinder.find_sex,
                'birth_day': vkinder.age_current[0],
                'birth_month': vkinder.age_current[1],
                'birth_year': vkinder.age_min,
                'has_photo': 1,
                'fields': fields
            }
        )
        return errors, result

    def find_users_groups(self, users_keys):
        """
        С помощью API execute получаем все группы всех пользователей за 1 вызов. Возвращаем словарь.
        """
        groups, errors = vk_api.vk_request_one_param_pool(
            self.vk_session,
            'groups.get',   # Метод
            key='user_id',  # Изменяющийся параметр
            values=users_keys,
            default_values={'count': 1000}
        )
        return errors, groups


if __name__ == '__main__':
    pass
