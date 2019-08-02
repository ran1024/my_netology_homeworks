from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView

from .models import Products, ProductCategory
from .forms import CustomerLoginForm, ResponseForm
from cart.forms import CartAddProductForm
from cart.cart import Cart


def main_page(request):
    """ Главная страница магазина """
    template = 'index_body.html'
    pr1 = Prefetch('products_set', queryset=Products.objects.filter(is_top=True))
    categories = get_list_or_404(ProductCategory.objects.prefetch_related(pr1).all())
    cart_product_form = CartAddProductForm(initial={'quantity': 1})
    context = {'items': categories, 'cart_product_form': cart_product_form}

    return render(request, template, context)


def show_category(request, category_id, brand_id):
    """ Вывод по категориям товаров """
    template = 'category_view.html'
    products = Products.objects.select_related('brand').filter(category=category_id, is_active=True)
    brands = list({x.brand for x in products})
    context = {
        'category_id': int(category_id),
        'brands': sorted(brands, key=lambda x: x.name),
    }
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


class ProductDetailView(DetailView):
    """ Страница с детальной информацией по товару, формой заказа и отзывами """
    template_name = 'product_detail.html'
    model = Products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        prod_num = cart.get_product_quantity(str(self.kwargs['pk']))
        context['cart_product_form'] = CartAddProductForm(initial={'quantity': prod_num})
        context['responses'] = context['object'].responses_set.all()
        context['response_form'] = ResponseForm()
        return context


@require_POST
def response_add(request, product_id):
    """ Функция сохраняет отзыв в базе данных """
    product = get_object_or_404(Products, pk=product_id)
    form = ResponseForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        print(data)
        response = form.save(commit=False)
        response.product = product
        response.save()
    return redirect('product_detail', product_id)


def data_for_context(request):
    """ Обработчик контекста """
    cart = Cart(request)
    categories = ProductCategory.objects.values('id', 'name')
    context = {
        'prod_num': cart.get_total_quantity(),
        'is_login': 'Войти',
        'categories': categories,
        }
    if request.user.is_authenticated:
        context['is_login'] = 'Выйти'
    return context


def customer_login(request):
    template = 'login.html'
    context = {'next': request.GET['next']}
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email'].split('@')
            password = form.cleaned_data['password']
            user = authenticate(username=username[0], password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.POST['next'])
                else:
                    context['error'] = 'Пользователь заблокирован администратором системы.'
            else:
                context['error'] = 'Учётные данные не верны.'
    form = CustomerLoginForm()
    context['form'] = form
    return render(request, template, context)


def customer_logout(request):
    session_cart = request.session['cart']
    template = 'logout.html'
    context = {'next': request.GET['next'], 'user': request.user.username}
    logout(request)
    request.session['cart'] = session_cart
    return render(request, template, context)
