from django.shortcuts import render
from django.conf import settings

import csv

def inflation_view(request):
    template_name = 'inflation.html'
    context = {}
    list_items = []

    # чтение csv-файла и заполнение контекста
    with open(settings.CSV_FILE) as fh:
        rows = list(csv.reader(fh, delimiter=';'))

    context['keys'] = rows.pop(0)
    for array in rows:
        list_items.append([float(a) for a in array if a])
    context['list_items'] = list_items

    return render(request, template_name, context)
