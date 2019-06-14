from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=30, verbose_name='Модель')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    image = models.URLField(verbose_name='url изображения')
    release_date = models.DateField(verbose_name='Дата релиза')
    lte_exists = models.BooleanField(default=False, verbose_name='Наличие LTE')
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, verbose_name='URL')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Телефоны'
        verbose_name = 'Телефон'

