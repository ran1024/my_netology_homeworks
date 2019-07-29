from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from shop.models import Products
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
    """ Функция показывает корзину. Если корзина пуста, блокируем кнопку заказа. """
    cart = Cart(request)
    is_empty = False
    if cart.get_total_quantity() == 0:
        is_empty = True
    return render(request, 'cart/cart.html', {'cart': cart, 'is_empty': is_empty})


def cart_clear(request):
    """ Полная очистка корзины """
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

