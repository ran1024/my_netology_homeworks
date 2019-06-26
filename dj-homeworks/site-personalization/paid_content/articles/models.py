from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=False, verbose_name='Прошёл активацию2?')
    is_subscribe = models.BooleanField(default=False, verbose_name='Подписался?')

    class Meta(AbstractUser.Meta):
        pass


class Article(models.Model):
    title = models.CharField(default='Здесь название статьи', max_length=250,
                             verbose_name='Заголовок статьи', help_text='Введите название статьи.')
    body = models.TextField(null=True, blank=True, verbose_name='Статья')
    is_paid = models.BooleanField(default=False, verbose_name='Платная')
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['-id']
