#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2_2_classes.py
#

class Animals:

    def __init__(self, animal, name, weight):
        if animal in ('гусь', 'курица', 'утка', 'корова', 'баран', 'коза'):
            self.animal = animal
            self.name = name
            self.weight = weight
        else:
            exit(1)

    def get_info(self):
        return "Это {}, вес: {}кг.".format(self.animal, self.weight)

    def get_weight(self):
        return self.weight

    def get_animal(self):
        return self.animal

    def get_name(self):
        return self.name

    def do_feed(self):
        self.weight += 0.2
        return "{} покормлена. Вес: {}кг.".format(self.animal.capitalize(), self.weight)

    def get_voice(self):
        if self.animal == 'гусь':
            return "Га-га-га"
        elif self.animal == 'курица':
            return "Ко-ко-ко"
        elif self.animal == 'утка':
            return "Кря-кря-кря"
        if self.animal == 'корова':
            return "Му-у-у..."
        elif self.animal == 'баран':
            return "Бе-е-е..."
        elif self.animal == 'коза':
            return "Ме-е-е..."


class Bird(Animals):

    def __init__(self, animal, name, weight=1):
        super().__init__(animal, name, weight)

    def get_eggs(self):
        self.weight -= 0.07
        return "Собрано 1 яйцо. Вес: {}кг.".format(round(self.weight, 2))


class Hoofed(Animals):

    def __init__(self, animal, name, weight=15):
        super().__init__(animal, name, weight)

    def get_milk(self):
        if self.animal == 'корова':
            self.weight -= 5
        elif self.animal == 'коза':
            self.weight -= 1.5
        else:
            return "Баранов не доят!"
        return "{0} подоена. Вес: {1}кг.".format(self.animal.capitalize(), self.weight)

    def get_wool(self):
        if self.animal == 'баран':
            return "{} подстрижен.".format(self.animal.capitalize())
        else:
            return "Этих не стигут!"


def main():

    chicken1 = Bird('курица', 'Ко-ко', 1.1)
    chicken2 = Bird('курица', 'Кукареку')
    goose_grey = Bird('гусь', 'Серый', 1.5)
    goose_white = Bird('гусь', 'Белый', 2.0)
    duck = Bird('утка', 'Кряква', 1.3)
    cow = Hoofed('корова', 'Манька', 350)
    sheep1 = Hoofed('баран', 'Барашек')
    sheep2 = Hoofed('баран', 'Кудрявый')
    goat1 = Hoofed('коза', 'Рога')
    goat2 = Hoofed('коза', 'Копыта')

    birds = [chicken1, chicken2, goose_grey, goose_white, duck]
    hoofeds = [cow, sheep1, sheep2, goat1, goat2]
    all_animals = birds + hoofeds

    for bird in birds:
        print("{0} Зовут {1}.".format(bird.get_info(), bird.get_name()))
        print(bird.do_feed())
        print(bird.get_eggs())
        print(bird.get_voice(), '\n')

    for hoofed in hoofeds:
        print("{0} Зовут {1}.".format(hoofed.get_info(), hoofed.get_name()))
        print(hoofed.do_feed())
        print(hoofed.get_milk())
        print(hoofed.get_wool())
        print(hoofed.get_voice(), '\n')

    max_weight = all_weight = 0
    max_name = max_animal = ''
    for animal in all_animals:
        all_weight += animal.get_weight()
        if max_weight < animal.get_weight():
            max_weight = animal.get_weight()
            max_animal = animal.get_animal()
            max_name = animal.get_name()
    print("Общий вес животных: {}кг.".format(round(all_weight, 2)))
    print("Самое тяжёлое животное: {0} {1} весит {2}кг".format(max_animal, max_name, max_weight))

main()
