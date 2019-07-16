from django import forms


class CartAddProductForm(forms.Form):
    """ Форма для выбора количества товаров. """
    quantity = forms.IntegerField(min_value=1, max_value=20, label='')
    # required_css_class = 'btn btn-primary'
