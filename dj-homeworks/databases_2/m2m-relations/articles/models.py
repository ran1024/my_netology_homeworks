from django.db import models


class Rubric(models.Model):

    name = models.CharField(max_length=30, help_text='Укажите рубрику', verbose_name='Рубрика')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    rubrics = models.ManyToManyField(Rubric, through='Relations', help_text='Укажите рубрику',
                                     verbose_name='Рубрика')

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Relations(models.Model):
    
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, help_text='Укажите рубрику для статьи',
                               verbose_name='Рубрика')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False, verbose_name='Основная')

    class Meta:
        verbose_name = 'Рубрику'
        verbose_name_plural = 'Все рубрики статьи'
