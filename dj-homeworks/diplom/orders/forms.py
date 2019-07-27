from django import forms
from .models import Orders
from shop.models import Customers


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('email', 'password', 'name', 'surname', 'phone', 'address')


class CustomerIsLoginForm(forms.ModelForm):
    email = forms.EmailField(label='', disabled=True,)

    class Meta:
        model = Customers
        fields = ('email', 'name', 'surname', 'phone', 'address')


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('comments',)