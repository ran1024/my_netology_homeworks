from django import forms


class CartAddProductForm(forms.Form):
    """ Форма для выбора количества товаров. """
    # update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, max_value=20, label='')
    required_css_class = 'btn btn-primary'
