from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings

import csv

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    bus_station = []
    ind = request.GET.get('page')
    ind = int(ind) if ind else 1
    prev_page = f'bus_stations?page={ind - 1}' if ind != 1 else None 

    current_page = ind
    next_page = f'bus_stations?page={ind + 1}'
    offset = 0

    with open(settings.BUS_STATION_CSV, encoding='cp1251') as fh:
        reader = list(csv.DictReader(fh))
        if ind*10 > len(reader):
            next_page = None
        arr = reader[(ind*10-10):(ind*10)]
        for row in arr:
            bus_station.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})

    return render_to_response('index.html', context={
        'bus_stations': bus_station,
        'current_page': current_page,
        'prev_page_url': prev_page,
        'next_page_url': next_page,
    })

