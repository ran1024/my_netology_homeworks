from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Prefetch
from django.core.paginator import Paginator

from .models import *
from .forms import CustomerLoginForm
from cart.forms import CartAddProductForm
from cart.cart import Cart


def _get_data(category_id):
    category = get_object_or_404(ProductCategory.objects.values('id', 'name'), pk=category_id)
    products = Products.objects.select_related('brand').filter(category=category_id, is_active=True)
    brands = list({x.brand for x in products})
    context = {'category': category,
               'items': sorted(brands, key=lambda x: x.name),
               }
    return products, context


def main_page(request):
    """ Главная страница магазина """
    template = 'index_body.html'
    pr1 = Prefetch('products_set', queryset=Products.objects.filter(is_top=True))
    categories = get_list_or_404(ProductCategory.objects.prefetch_related(pr1).all())
    cart_product_form = CartAddProductForm(initial={'quantity': 1})
    context = {'items': categories, 'cart_product_form': cart_product_form}

    return render(request, template, context)


def show_category(request, id, brand_id):
    """ Вывод по категориям товаров """
    template = 'category_view.html'
    products, context = _get_data(id)
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

    context = {'items': categories,
               'cart_product_form': cart_product_form,
               'product': get_object_or_404(Products, pk=product_id)
               }
    return render(request, template, context)


def data_for_context(request):
    """ Обработчик контекста """
    cart = Cart(request)
    context = {'category': {'name': 'Список разделов', 'id': 0},
               'prod_num': cart.get_total_quantity(),
               'is_login': 'Войти',
               }
    if request.session.get('customer'):
        context['is_login'] = 'Выйти'
    return context


def customer_login(request):
    template = 'login.html'
    context = {'next': request.GET['next']}
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            if Customers.objects.filter(email=form.cleaned_data['email']).exists():
                customer = Customers.objects.get(email=form.cleaned_data['email'])
                if customer.password == form.cleaned_data['password']:
                    session = request.session
                    session['customer'] = customer.id
                    return redirect(request.POST['next'])
                else:
                    context['error'] = 'Учётные данные не верны.'
            else:
                context['error'] = 'Данный пользователь не зарегистрирован.'
    form = CustomerLoginForm()
    context['form'] = form
    return render(request, template, context)


def customer_logout(request):
    template = 'logout.html'
    context = {'next': request.GET['next']}
    del request.session['customer']
    return render(request, template, context)
