from django.db import models


class Player(models.Model):
    is_main = models.BooleanField(default=False, verbose_name='Является главным игроком?')
    game = models.ManyToManyField('Game', through='PlayerGameInfo', verbose_name='Текущая игра')


class Game(models.Model):
    number = models.IntegerField(verbose_name='Загаданное число')
    counts = models.IntegerField(default=0, verbose_name='Счётчик попыток')
    status = models.IntegerField(verbose_name='статус игры: 1-ожидние,2-в процессе,3-окончена')


class PlayerGameInfo(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')

