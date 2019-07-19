from django import forms
from .models import ProductCategory, Products, Responses

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


class ResponseForm(forms.ModelForm):
    name = forms.CharField(label='Имя', min_length=1, max_length=20)
    comment = forms.CharField(label='Содержание', widget=forms.Textarea)
    ORDER_NUM = {
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    }
    rating = forms.TypedChoiceField(label='', choices=sorted(ORDER_NUM), widget=forms.RadioSelect)

    name.widget.attrs.update({'class': 'form-control', 'placeholder': 'Представтесь'})
    comment.widget.attrs.update({'class': 'form-control', 'placeholder': 'Содержание'})
    rating.widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Responses
        fields = ('name', 'comment', 'rating',)
