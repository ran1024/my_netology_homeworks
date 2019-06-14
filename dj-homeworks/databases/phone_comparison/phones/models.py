from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=20, verbose_name='Производитель')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Фирмы производители'
        verbose_name = 'Фирма производитель'
        ordering = ['name']
    

class Phone(models.Model):
    vendorname = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, verbose_name='Производитель')
    model = models.CharField(max_length=20, verbose_name='Модель')
    price = models.IntegerField(verbose_name='Цена')
    os = models.CharField(max_length=15, verbose_name='Операционная система')
    typesim = models.CharField(max_length=15, verbose_name='Тип SIM-карт')
    numsim = models.CharField(max_length=1, verbose_name='Количество SIM-карт')
    screendiag = models.CharField(max_length=8, verbose_name='Диагональ экрана')
    screenres = models.CharField(max_length=10, verbose_name='Разрешение экрана')
    density = models.CharField(max_length=8, verbose_name='Плотность пикселей')
    proc = models.CharField(max_length=30, verbose_name='Процессор')
    memory = models.CharField(max_length=5, verbose_name='Объём оперативной памяти')
    nfc = models.BooleanField(default=False, verbose_name='NFC')
    glonas = models.BooleanField(default=False, verbose_name='ГЛОНАСС')
    gps = models.BooleanField(default=False, verbose_name='GPS')
    fmradio = models.BooleanField(default=False, verbose_name='FM-Радио')
    
    def __str__(self):
        return f'{self.vendorname.name} {self.model}'
    
    class Meta:
        verbose_name_plural = 'Смартфоны'
        verbose_name = 'Смартфон'
        ordering = ['vendorname', 'model']
    

class Samsung(models.Model):
    additional = models.TextField(null=True, blank=True, verbose_name='Дополнительно', help_text='Дополнительные особенности и уникальные характеристики')
    phone = models.ForeignKey('Phone', null=True, on_delete=models.CASCADE)
    
    
class Xiaomi(models.Model):
    additional = models.TextField(null=True, blank=True, verbose_name='Дополнительно', help_text='Дополнительные особенности и уникальные характеристики')
    phone = models.ForeignKey('Phone', null=True, on_delete=models.CASCADE)


class Asus(models.Model):
    additional = models.TextField(null=True, blank=True, verbose_name='Дополнительно', help_text='Дополнительные особенности и уникальные характеристики')
    phone = models.ForeignKey('Phone', null=True, on_delete=models.CASCADE)
