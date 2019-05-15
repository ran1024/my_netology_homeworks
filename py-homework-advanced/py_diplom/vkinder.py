#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file-name.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import json
import dbworker
from time import sleep
from datetime import date
from vksession import VkSession


class Vkinder:

    def __init__(self):
        self.id = ''
        self.first_name = ''
        self.last_name = ''
        self.screen_name = ''
        self.login = ''
        self.city = {}
        self.interests = []
        self.music = []
        self.movies = []
        self.books = []
        self.groups = set()
        self.token = ''
        self.age_min = 0
        self.age_max = 0
        self.find_sex = ''
        self.find_city = {}
        self.age_current = [1, 1]
        self.find_interests = []

    def __str__(self):
        return f' {{\n\tid: {self.id},\n\tfirst_name: {self.first_name}\n\tlast_name: {self.last_name}\n\t' \
            f'screen_name: {self.screen_name}\n\tlogin: {self.login}\n\tcity: {self.city}\n\t' \
            f'interests: {self.interests}\n\tmusic: {self.music}\n\tmovies: {self.movies}\n\t' \
            f'books: {self.books}\n\tgroups: {self.groups}\n\ttoken: {self.token}\n\t' \
            f'age_min: {self.age_min}\n\tage_max: {self.age_max}\n\tage_current: {self.age_current}\n\t' \
            f'find_sex: {self.find_sex}\n\tfind_city: {self.find_city}\n\t' \
            f'find_interests: {self.find_interests}\n }}'


def if_error(result):
    if result[0]:
        print(f'Произошла ошибка авторизации: {result[1]}.\n Попробуйте ещё раз.')
        return 1
    else:
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
        result = dbworker.find_vkinder(vkinder, login)
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
            # Всегда запрашиваем данные пользователя в ВК
            # т.к. они могли измениться с момента предыдущего запуска.
            user_data = vk_connect.get_user_data()
            # Если у пользователя ВК не указан город:
            if 'city' not in user_data and not vkinder.city:
                err = 1
                while err:
                    city_title = input('Введите город проживания: ')
                    err, city = vk_connect.find_city(city_title)
                    user_data['city'] = city
            dbworker.update_user(vkinder, login, user_data)


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
        err, city = vk_connect.find_city(city_title)
        find_city = vkinder.city if err else city
    else:
        find_city = vkinder.city

    interests = input('Введите желаемые интересы через запятую: ').split(',')

    year = date.today().year
    if age_max <= age_min:
        age_min = age_max = year - age_min
    else:
        age_min = year - age_min
        age_max = year - age_max

    vkinder.age_current = [1, 1]
    find_data = {'age_min': age_min, 'age_max': age_max,
                 'find_sex': sex, 'find_city': find_city, 'find_interests': interests}
    dbworker.update_find_params(vkinder, find_data)
    return 0


def prepare_user(item, relation):
    """
    Подготавливаем профиль найденного пользователя к показу и считаем его рейтинг.
    """
    rating = 0
    item_dict = {
        'Реципиент': f'{item["first_name"]} {item["last_name"]}',
        'Фотография': item['photo_max_orig'],
        'Адрес в ВК': f'https://vk.com/id{item["id"]}',
        'id': item['id'],
        'select': 0,
    }
    if 'relation' in item:
        item_dict['Семейное положение'] = relation[item['relation']][1]
        rating += relation[item['relation']][0]
    if 'occupation' in item:
        if item['occupation']['type'] == 'university':
            item_dict['Образование'] = f'высшее: {item["occupation"]["name"]}'
        elif item['occupation']['type'] == 'work':
            item_dict['Работает в'] = item['occupation']['name']
        elif item['occupation']['type'] == 'school':
            item_dict['Образование'] = f'школа: {item["occupation"]["name"]}'
    if item['is_friend']:
        item_dict['Является ли Вашим другом'] = 'да'
        rating += 5
    else:
        item_dict['Является ли Вашим другом'] = 'нет'
    if item['common_count']:
        rating += item['common_count']
    item_dict['Количество общих друзей'] = item['common_count']

    item_dict['rating'] = rating
    return item_dict


def users_search(vkinder, vk_connect):
    """
    Функция производит поиск в 'ВК', получает группы всех реципиентов и
    находит количество общих с данным пользователем. Затем подсчитывает
    рейтинг каждой записи и сортирует записи по рейтигу.
    """
    relation = {
        0: (1, 'не указано'),
        1: (4, 'в браке не состоит'),
        2: (2, 'есть друг или подруга'),
        3: (1, 'помолвлен / помолвлена'),
        4: (0, 'состоит в браке'),
        5: (3, 'всё сложно'),
        6: (5, 'в активном поиске'),
        7: (2, 'влюблён / влюблена'),
        8: (0, 'в гражданском браке')
    }
    users = {}
    err, result = vk_connect.find_users(vkinder)
    if err:
        print('Поиск не удался. Попробуйте позже.')
        exit(code=1)
    for val in result.values():
        for item in val['items']:
            # Отсеиваем полностью закрытые профили и тех, кто не афиширует семейное положение.
            if item['is_closed'] and not item['can_access_closed'] or 'relation' not in item:
                continue
            item_dict = prepare_user(item, relation)
            users[item['id']] = item_dict

    # Получаем группы всех реципиентов и находим количество общих с данным пользователем.
    errors, groups = vk_connect.find_users_groups(list(users.keys()))
    if not len(errors):
        for key, value in groups.items():
            user_groups = set(value['items'])
            user_groups &= vkinder.groups
            users[key]['rating'] += len(user_groups)
            users[key]['Количество общих групп'] = len(user_groups)

    # Обновляем базу реципиентов, а в атрибуты vkinder заносим offset.
    if vkinder.age_current[0] == 0:
        vkinder.age_current = [1, vkinder.age_current[1] + 1]
    else:
        vkinder.age_current[0] += 1
    dbworker.update_vkusers(vkinder, users)
    # Сортируем список реципиентов по рейтингу.
    return sorted(users.values(), key=lambda x: x['rating'], reverse=True)


def print_users(vk_connect, users):
    """
    # Выводим на атрибуты найденных людей на консоль и организуем диалог с пользователем
    по выбору понравившихся, показываем топ-3 фотографии из каждого альбома реципиента.
    """
    for user in users:
        result = dbworker.search_vkuser(user['id'])
        if 'select' in result and result['select'] == 2:
            continue
        for key, val in user.items():
            if key == 'id' or key == 'select':
                continue
            if key == 'select' and val == 1:
                val = 'В избранном!'
            print(f'{key}: {val}')
        print('\n')
        select = 0
        while not select:
            try:
                select = int(input('Оцените эту находку (1 - В избранное! / 2 - Никогда больше не видеть!): '))
                if select not in [1, 2]:
                    select = 0
            except (ValueError, KeyError):
                select = 0
        dbworker.update_vkuser(user['id'], {'select': select})
        print('\n')


def calculate_offset(vkinder):
    if vkinder.age_current[1] >= 13:
        vkinder.age_current = [1, 1]
        vkinder.age_min -= 1
    if vkinder.age_current[0] >= 29 and vkinder.age_current[1] == 2:
        vkinder.age_current = [1, 3]
    elif vkinder.age_current[0] >= 31 and vkinder.age_current[1] in [4, 6, 9, 11]:
        vkinder.age_current = [1, vkinder.age_current[1] + 1]
    elif vkinder.age_current[0] >= 32:
        vkinder.age_current = [1, vkinder.age_current[1] + 1]
    return vkinder.age_min < vkinder.age_max


def out_json(vk_connect, users):
    for user in users[:10]:
        user['photos'] = vk_connect.get_albums(user['id'])
    out_str = json.dumps(users[:10], indent=1, ensure_ascii=False)
    try:
        with open('groups.json', "w") as fh:
            fh.write(out_str)
    except EnvironmentError as err:
        print('Не удалось записать результат в файл "groups.json".', err)


def begin_search(vkinder, vk_connect):
    print(f'Параметры:\nГод рождения: {vkinder.age_min} - {vkinder.age_max}')
    sex = 'женский' if vkinder.find_sex == 1 else 'мужской'
    print(f'Пол: {sex}\n'
          f'Город: {vkinder.find_city["title"]}\n'
          f'Интересы: {vkinder.find_interests}\n')

    users = []
    while len(users) < 10:
        if calculate_offset(vkinder):
            print('Поиск закончен. Вы можете ввести другие параметры поиска.')
            return 0
        print(f'Производится поиск: {vkinder.age_current[0]}-{vkinder.age_current[1]}-{vkinder.age_min}')
        # Задержка от отключения нас от АПИ ВК.
        sleep(15)
        users += users_search(vkinder, vk_connect)
        # если за этот день найдено < 10 человек, то искать за весь месяц сразу.
        if len(users) < 10:
            vkinder.age_current[0] = 0
        print(f' найдено {len(users)} человек.')
    if users:
        # Выводим в json:
        out_json(vk_connect, users)
        # Выводим на консоль и организуем диалог с пользователем.
        print_users(vk_connect, users)
    else:
        print('С такими параметрами ничего не найдено.')


def new_search(vkinder, vk_connect):
    result = 1
    while result:
        result = get_find_params(vkinder, vk_connect)
        if result:
            print('\nБыли введены неправильные параметры! Попробуйте ещё раз.\n')
    print('\nПроизводится поиск.')
    begin_search(vkinder, vk_connect)


def next_search(vkinder, vk_connect):
    print('\nПродолжается поиск.')
    begin_search(vkinder, vk_connect)


def main():
    functions = dict(new=new_search, next=next_search)
    vkinder = Vkinder()
    vk_connect = VkSession()
    user_login(vkinder, vk_connect)

    if vkinder.age_min:
        print(f'\nПрошлые параметры поиска:\n'
              f'Год рождения: {vkinder.age_min} - {vkinder.age_max}')
        sex = 'женский' if vkinder.find_sex == 1 else 'мужской'
        print(f'Пол: {sex}\n'
              f'Город: {vkinder.find_city["title"]}\n'
              f'Интересы: {vkinder.find_interests}\n')
        answer = input('Продолжить поиск с этими параметрами? (Y / N): ').lower()
        if answer == 'y':
            begin_search(vkinder, vk_connect)
    else:
        new_search(vkinder, vk_connect)

    while True:
        print('Введите команду: new - новый поиск, next - искать дальше, quit - выход из программы')
        comm = input('Ввод: ')
        if comm in functions:
            functions[comm](vkinder, vk_connect)
        elif comm == 'quit':
            break
        else:
            print('Введена недопустимая команда!')


if __name__ == '__main__':
    import sys
    sys.exit(main())
