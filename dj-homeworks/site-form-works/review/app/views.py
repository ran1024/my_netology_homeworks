from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            if 'reviewed_product' in request.session:
                cnt = request.session['reviewed_product']
            else:
                cnt = []
            cnt.append(product.id)
            request.session['reviewed_product'] = cnt
            return redirect('main_page')
        else:
            context = {'form': form, 'product': product}
    else:
        form = ReviewForm()
        context = {'form': form, 'product': product, 'visible': 'block'}
        if  'reviewed_product' in request.session:
            cnt = request.session['reviewed_product']
            if product.id in cnt:
                context['is_review_exist'] = 1
                context['visible'] = 'none'

    return render(request, template, context)
