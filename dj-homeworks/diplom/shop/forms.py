from django import forms
from .models import ProductCategory, Products, Customers

from ckeditor.widgets import CKEditorWidget


class ProductCategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Статья')

    class Meta:
        model = ProductCategory
        fields = ('name', 'description')


class ProductsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Статья')

    class Meta:
        model = Products
        fields = ('description',)


class CustomerLoginForm(forms.Form):
    email = forms.EmailField(label='')
    password = forms.CharField(min_length=1, max_length=20, label='',
                               strip=True, widget=forms.PasswordInput)

    email.widget.attrs.update({'class': 'form-control',
                               'placeholder': 'Email',
                               'autofocus': True,
                               })
    password.widget.attrs.update({'class': 'form-control',
                                  'placeholder': 'Пароль',
                                  })
