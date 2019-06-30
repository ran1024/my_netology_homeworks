from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создание суперпользователя.'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs=1, type=str)
        parser.add_argument('email', nargs=1, type=str)
        parser.add_argument('password', nargs=1, type=str)

    def handle(self, *args, **options):
        username = options['username'][0]
        email = options['email'][0]
        password = options['password'][0]
        print(username, email, password)
        if User.objects.filter(username=username).count() == 0:
            User.objects.create_superuser(username, email, password);
            print('Суперпользователь создан')
        else:
            print('Пользоатель с таким именем уже есть.')
