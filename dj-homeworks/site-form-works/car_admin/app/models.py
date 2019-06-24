from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=50, verbose_name='Производитель')
    model = models.CharField(max_length=50, verbose_name='Модель')

    def __str__(self):
        return f'{self.brand} {self.model}'

    def review_count(self):
        return Review.objects.filter(car=self).count()
        
    class Meta:
        verbose_name_plural = 'Автомобили'
        verbose_name = 'Автомобиль'
        ordering = ['-id']


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(null=True, blank=True, verbose_name='Статья')

    def __str__(self):
        return str(self.car) + ' ' + self.title
        
    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['-id']

