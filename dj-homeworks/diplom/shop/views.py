from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Prefetch
from django.core.paginator import Paginator

from .models import *
from cart.forms import CartAddProductForm
from cart.cart import Cart


def _get_context(request):
    """ Формируем контекст """
    cart = Cart(request)
    arr = {'name': 'Список разделов', 'id': 0}
    context = {'category': arr, 'prod_num': cart.get_total_quantity()}
    return context


def _get_data(request, category_id):
    category = get_object_or_404(ProductCategory.objects.values('id', 'name'), pk=category_id)
    products = Products.objects.select_related('brand').filter(category=category_id, is_active=True)
    brands = list({x.brand for x in products})
    context = _get_context(request)
    context['items'] = sorted(brands, key=lambda x: x.name)
    context['category'] = category
    return products, context


def main_page(request):
    """ Главная страница магазина """
    template = 'index_body.html'
    pr1 = Prefetch('products_set', queryset=Products.objects.filter(is_top=True))
    categories = get_list_or_404(ProductCategory.objects.prefetch_related(pr1).all())
    context = _get_context(request)
    context['items'] = categories
    cart_product_form = CartAddProductForm(initial={'quantity': 1})
    context['cart_product_form'] = cart_product_form

    return render(request, template, context)


def show_category(request, id, brand_id):
    """ Вывод по категориям товаров """
    template = 'category_view.html'
    products, context = _get_data(request, id)
    cart_product_form = CartAddProductForm(initial={'quantity': 1})
    context['cart_product_form'] = cart_product_form

    if int(brand_id) != 0:
        paginator = Paginator(products.filter(brand=brand_id), 6)
    else:
        paginator = Paginator(products, 6)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    list_pages = [x+1 for x in range(paginator.num_pages)]
    context['list_pages'] = list_pages
    context['products'] = page.object_list
    context['page'] = page

    return render(request, template, context)


def product_detail(request, product_id):
    """ Страница с детальной информацией по товару и кнопкой заказа """
    template = 'product_detail.html'
    cart = Cart(request)
    prod_num = cart.get_product_quantity(product_id)
    cart_product_form = CartAddProductForm(initial={'quantity': prod_num})
    categories = get_list_or_404(ProductCategory.objects.values('id', 'name'))
    context = _get_context(request)
    context['items'] = categories
    context['product'] = get_object_or_404(Products, pk=product_id)
    context['cart_product_form'] = cart_product_form
    return render(request, template, context)
