from django.contrib import admin
from django.urls import reverse
from .models import ProductCategory, ProductBrand, Products, Responses, Customer
from .forms import ProductCategoryAdminForm, ProductsAdminForm


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Responses)
class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('created', 'product', 'name', 'comment', 'rating')
    ordering = ('created', 'product')
    list_filter = ('rating',)


class ProductsInline(admin.TabularInline):
    model = Products
    fields = ('is_top', 'name', 'brand', 'quantity', 'price', 'created')
    readonly_fields = ('brand', 'name', 'quantity', 'price', 'created',)
    extra = 0
    fk_name = 'category'
    can_delete = False
    verbose_name_plural = 'Список товаров в данной категории'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    form = ProductCategoryAdminForm
    ordering = ('name',)
    search_fields = ('name',)
    inlines = [ProductsInline]


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = ('name', 'quantity', 'price', 'created', 'category', 'is_top', 'is_active')
    list_filter = ('category', 'brand', 'is_top', 'is_active')
    search_fields = ('name',)
    fields = (('category', 'is_top', 'is_active'), 'brand', ('name', 'created'), 'quantity', 'price',
              'short_text', 'description', 'image')
    readonly_fields = ('created',)
    radio_fields = {'category': admin.HORIZONTAL}

    def view_on_site(self, rec):
        return reverse('product_detail', kwargs={'pk': rec.pk})
