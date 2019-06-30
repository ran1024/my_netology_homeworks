# Generated by Django 2.2.1 on 2019-06-30 02:33

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fields_for_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12, verbose_name='Имя поля')),
                ('width', models.SmallIntegerField(verbose_name='ширина поля')),
            ],
            options={
                'verbose_name': 'Поле таблицы',
                'verbose_name_plural': 'Поля для таблицы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Filecsv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=30, verbose_name='Путь к файлу')),
            ],
            managers=[
                ('wrk_path', django.db.models.manager.Manager()),
            ],
        ),
    ]
