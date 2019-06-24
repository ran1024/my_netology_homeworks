from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    is_login = models.BooleanFoeld(default=False, verbose_name='Залогинился?')
    is_subscribe = models.BooleanFoeld(default=False, verbose_name='Подписался?')
    
    class Meta(AbstractUser.Meta):
        pass


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок статьи', help_text='Введите название статьи.')
    body = models.TextField(verbose_name='Статья')
    is_paid = models.BooleanFoeld(default=False, verbose_name='Платная')
