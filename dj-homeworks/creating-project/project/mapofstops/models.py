from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название остановки, адрес')
    latitude = models.FloatField(default=0, verbose_name='Широта')
    longitude = models.FloatField(default=0, verbose_name='Долгота')
    routes = models.ManyToManyField('Route', verbose_name='Номера маршрутов')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Автобусная остановка'
        verbose_name_plural = 'Автобусные остановки'

    def __str__(self):
        return self.name
    
    
class Route(models.Model):
    name = models.CharField(max_length=6, verbose_name='Номер маршрута')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Номер маршрута'
        verbose_name_plural = 'Номера маршрутов'

    def __str__(self):
        return self.name
