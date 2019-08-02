from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(max_length=256, verbose_name='Адрес')

    class Meta(AbstractUser.Meta):
        pass


class ProductCategory(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Категория товара')
    description = models.TextField(blank=True, null=True, default=None, verbose_name='Статья')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории товаров'


class ProductBrand(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Бренд')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Products(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование товара')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='Бренд')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    quantity = models.SmallIntegerField(default=0, verbose_name='Количество на складе')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    short_text = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, default=None, verbose_name='Описание')
    image = models.ImageField(upload_to='', verbose_name='Изображение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')
    is_active = models.BooleanField(default=True, verbose_name='В продаже')
    is_top = models.BooleanField(default=False, verbose_name='Топ')
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
        index_together = ['category', 'is_active', 'is_top']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Responses(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Заказ')
    name = models.CharField(max_length=20, verbose_name='Имя')
    comment = models.TextField(blank=True, null=True, default=None, verbose_name='Содержание')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    class Meta:
        ordering = ['created']
        verbose_name = 'Отзыв на товар'
        verbose_name_plural = 'Отзывы на товар'
