import csv

from django.core.management.base import BaseCommand
from mapofstops.models import Station, Route


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файла.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file'][0]
        num_of_route = {}
        with open(csv_file, encoding='cp1251') as fh:
            reader = csv.reader(fh, delimiter=';')
            reader.__next__()
            for row in reader:
                list_route = [route.strip() for route in row[7].split(';')]
                for i, route in enumerate(list_route):
                    if route not in num_of_route:
                        num_of_route[route] = Route.objects.create(name=route)
                    list_route[i] = num_of_route[route]
                st = Station.objects.create(name=row[1], longitude=row[2], latitude=row[3])
                st.routes.add(*list_route)
