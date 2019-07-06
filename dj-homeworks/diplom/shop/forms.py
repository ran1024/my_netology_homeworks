from django import forms
from .models import ProductCategory, Products

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
        # fields = ('name', 'quantity', 'price', 'category', 'description')
        fields = ('description',)
