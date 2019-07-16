from django import forms
from shop.models import Orders


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('')
