from django.contrib import admin
from .models import *
from .forms import ProductCategoryAdminForm, ProductsAdminForm


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'phone', 'date_joined', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    form = ProductCategoryAdminForm
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(ProductBrand)
class ProductBrand(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = ('name', 'quantity', 'price', 'created', 'category')
    list_filter = ('category', 'brand')
    search_fields = ('name',)
    fields = ('category', 'brand', ('name', 'created'), 'quantity', 'price',
              'short_text', 'description', 'image')
    readonly_fields = ('created',)
    radio_fields = {'category': admin.HORIZONTAL}

