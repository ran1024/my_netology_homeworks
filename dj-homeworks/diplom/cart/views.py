from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from shop.models import Products, ProductCategory
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """ Функция добавляет товар в корзину """
    product = get_object_or_404(Products, pk=product_id)
    if product.quantity > 0:
        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cart.add(product=product, quantity=data['quantity'])
    else:
        messages.error(request, f'Извините, но товара {product.name} нет в наличии!')
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """ Функция удаляет товар из корзины """
    cart = Cart(request)
    product = get_object_or_404(Products, pk=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """ Функция показывает корзину """
    cart = Cart(request)
    context = {}
    # categories = ProductCategory.objects.values('id', 'name')
    # arr = {'name': 'Список разделов', 'id': 0}
    # context = {'items': categories, 'category': arr}
    context['cart'] = cart
    # context['prod_num'] = cart.get_total_quantity()

    return render(request, 'cart/cart.html', context)


def cart_clear(request):
    """ Полная очистка корзины """
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

