from django.shortcuts import render
from .models import Phone


def show_catalog(request):
    template = 'catalog.html'
    sort_ind = request.GET.get('sort')
    if sort_ind == 'name':
        phones = Phone.objects.order_by('name')
    elif sort_ind == 'min-price':
        phones = Phone.objects.order_by('price')
    elif sort_ind == 'max-price':
        phones = Phone.objects.order_by('price').reverse()
    else:
        phones = Phone.objects.all()
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
