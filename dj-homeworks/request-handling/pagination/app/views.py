from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings

import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as fh:
        reader = list(csv.DictReader(fh))

    paginator = Paginator(reader, 10)
    page = request.GET.get('page')
    p_pag = paginator.get_page(page)
    
    return render_to_response('index.html', context={'pag': p_pag})
