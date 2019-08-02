from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Orders
from shop.models import Customer


class CustomerForm(UserCreationForm):
    email = forms.EmailField(label='Эл.почта')

    class Meta:
        model = Customer
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address')


class CustomerIsLoginForm(forms.ModelForm):
    email = forms.EmailField(label='', disabled=True,)

    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', 'phone', 'address')


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('comments',)
