from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from shop.models import Customer, Products
from .models import ProductsInOrder
from .forms import OrderCreateForm, CustomerForm, CustomerIsLoginForm
from cart.cart import Cart


def order_create(request):
    template = 'orders/create.html'
    cart = Cart(request)
    form_errors = ''
    if request.user.is_authenticated:
        customer = request.user

        if request.method == 'POST':
            customer_form = CustomerIsLoginForm(request.POST, instance=customer)
            order_form = OrderCreateForm(request.POST)
            if order_form.is_valid() and customer_form.is_valid():
                if customer_form.has_changed():
                    customer_form.save()
                return _order_create(request, cart, order_form, customer)
            else:
                form_errors = dict(customer_form.errors)
                customer_form = CustomerIsLoginForm(instance=customer)
        else:
            customer_form = CustomerIsLoginForm(instance=customer)
    else:
        if request.method == 'POST':
            customer_form = CustomerForm(request.POST)
            order_form = OrderCreateForm(request.POST)
            if order_form.is_valid() and customer_form.is_valid():
                username, _ = customer_form.cleaned_data['email'].split('@')
                password = customer_form.cleaned_data['password1']

                user = customer_form.save(commit=False)
                user.username = username
                user.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return _order_create(request, cart, order_form, user)
            else:
                form_errors = dict(customer_form.errors)
                customer_form = CustomerForm()
        else:
            customer_form = CustomerForm()
    order_form = OrderCreateForm()
    context = {'cart': cart,
               'customer_form': customer_form,
               'order_form': order_form,
               'errors': form_errors}
    return render(request, template, context)


def _order_create(request, cart, order_form, user):
    """
    Создаём заказ. Уменьшаем количество товара на складе на число заказанных единиц.
    Если на складе товара меньше, чем заказано, удаляем заказ и извещаем покупателя.
    """
    order = order_form.save(commit=False)
    order.customer = user
    order.save()

    for item in cart:
        product = Products.objects.get(pk=item['id'])
        balance = product.quantity - item['quantity']
        if balance < 0:
            order.delete()
            messages.error(request, f'Извините, но такого количества товара'
                                    f' "{product.name}" нет в наличии! Осталось '
                                    f'{product.quantity} шт.')
            return redirect('cart:cart_detail')
        product.quantity = balance
        product.save(update_fields=['quantity'])

        ProductsInOrder.objects.create(order=order,
                                       product=product,
                                       number_of_units=item['quantity'],
                                       price_of_unit=item['price'],
                                       )
    cart.clear()
    return render(request, 'orders/created.html', {'order': order})
