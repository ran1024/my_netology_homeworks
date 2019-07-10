from django.shortcuts import render
from django.db.models import Prefetch

from .models import *


def main_page(request):
    template = 'index_body.html'
    pr1 = Prefetch('products_set', queryset=Products.objects.filter(is_top=True))
    categories = ProductCategory.objects.prefetch_related(pr1).all()
    arr = {'name': 'Список разделов', 'id': 0}
    context = {'items': categories, 'category': arr}
    return render(request, template, context)


def show_category(request, id, brand_id):
    template = 'category_view.html'
    category = ProductCategory.objects.values('id', 'name').get(pk=id)
    products = Products.objects.select_related('brand').filter(category=id)
    brands = list({x.brand for x in products})
    print(str(brands))
    context = {'items': sorted(brands, key=lambda x: x.name),
               'category': category,
               }
    if int(brand_id) != 0:
        context['products'] = products.filter(brand=brand_id)
    else:
        context['products'] = products

    return render(request, template, context)


def product_detail(request, id, product_id):
    print(id, product_id)
    template = 'product_detail.html'
    category = ProductCategory.objects.values('id', 'name').get(pk=id)
    products = Products.objects.select_related('brand').filter(category=id)
    brands = list({x.brand for x in products})
    context = {'items': sorted(brands, key=lambda x: x.name),
               'category': category,
               'product': products.get(pk=product_id)
               }

    return render(request, template, context)
