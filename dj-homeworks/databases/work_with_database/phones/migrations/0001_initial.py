# Generated by Django 2.2.1 on 2019-06-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Модель')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('image', models.URLField(verbose_name='url изображения')),
                ('release_date', models.DateField(verbose_name='Дата релиза')),
                ('lte_exists', models.BooleanField(default=False, verbose_name='Наличие LTE')),
                ('slug', models.SlugField(allow_unicode=True, max_length=200)),
            ],
        ),
    ]
