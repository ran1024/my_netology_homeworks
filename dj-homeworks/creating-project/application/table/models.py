from django.db import models


class Fieldsfortable(models.Model):
    name = models.CharField(max_length=12, verbose_name='Имя поля')
    width = models.SmallIntegerField(verbose_name='ширина поля')

    class Meta:
        verbose_name_plural = 'Поля для таблицы'
        verbose_name = 'Поле таблицы'
        ordering = ['id']

    def __str__(self):
        return f'имя: {self.name}, ширина: {self.width}'


class FilecsvManager(models.Manager):
    def get_path(self):
        if self.filter(pk=1).exists():
            rec = self.get(pk=1)
            return rec.file_path
        
    def set_path(self, path):
        self.filter(id=1).delete()
        file_path = self.create(id=1, file_path=path)
        return file_path
    

class Filecsv(models.Model):
    file_path = models.CharField(max_length=30, verbose_name='Путь к файлу')
    
    wrk_path = FilecsvManager()
    objects = models.Manager()
    
    def __str__(self):
        return self.file_path
