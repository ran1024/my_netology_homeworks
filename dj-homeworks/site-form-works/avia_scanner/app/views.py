# import time
# import random

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from .models import City
from .forms import SearchTicket


def ticket_page_view(request):
    template = 'app/ticket_page.html'

    context = {
        'form': SearchTicket()
    }

    return render(request, template, context)


def cities_lookup(request):
    """Ajax request предлагающий города для автоподстановки, возвращает JSON"""
    field_search = request.GET['term']
    cities = list(cache.get_or_set('cities', City.objects.values_list('name', flat=True)))
    results = [city for city in cities if city.startswith(field_search.capitalize())]

    return JsonResponse(results, safe=False)

