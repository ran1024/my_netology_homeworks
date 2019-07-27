# Generated by Django 2.2.1 on 2019-06-25 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Загаданное число')),
                ('counts', models.IntegerField(verbose_name='Счётчик попыток')),
                ('status', models.IntegerField(verbose_name='статус игры: 1-ожидние,2-в процессе,3-окончена')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=256, verbose_name='id сессии')),
                ('is_main', models.BooleanField(default=False, verbose_name='Является главным игроком?')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game', verbose_name='Игра')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Player', verbose_name='Игрок')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ManyToManyField(through='game.PlayerGameInfo', to='game.Game', verbose_name='Текущая игра'),
        ),
    ]