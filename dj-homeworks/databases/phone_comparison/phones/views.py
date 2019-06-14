from django.shortcuts import render
from .models import Phone, Asus, Samsung, Xiaomi


def show_catalog(request):
    template = 'catalog.html'
    asus = Asus.objects.first()
    samsung = Samsung.objects.first()
    xiaomi = Xiaomi.objects.first()
    context = {'asus': asus, 'samsung': samsung, 'xiaomi': xiaomi}
    return render(
        request,
        template,
        context
    )
