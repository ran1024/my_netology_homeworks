from django.contrib import admin
from .models import *
from .forms import ProductCategoryAdminForm, ProductsAdminForm


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'surname', 'phone', 'date_joined', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)


class ProductsInline(admin.TabularInline):
    model = Products
    fields = ('is_top', 'name', 'brand', 'quantity', 'price', 'created')
    readonly_fields = ('brand', 'name', 'quantity', 'price', 'created',)
    extra = 0
    fk_name = 'category'
    can_delete = False
    verbose_name_plural = 'Список товаров в данной категории'

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(quantity=14)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    form = ProductCategoryAdminForm
    ordering = ('name',)
    search_fields = ('name',)
    inlines = [ProductsInline]


@admin.register(ProductBrand)
class ProductBrand(admin.ModelAdmin):
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


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    fields = ('product', 'number_of_units', 'price_of_unit', 'total_amount')
    extra = 0
    verbose_name_plural = 'Список товаров в заказе'


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'customer', 'total_number', 'total_price',
                    'status', 'is_comments')
    list_display_links = ('id', 'created', 'customer')
    list_select_related = True
    list_filter = ('status',)
    search_fields = ('id',)
    date_hierarchy = 'created'
    inlines = (ProductsInOrderInline,)

    def is_comments(self, rec):
        result = 'Да' if rec.comments else '---'
        return result

    is_comments.short_description = 'Комментарий'


@admin.register(ProductsInOrder)
class ProductsInOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'number_of_units', 'price_of_unit', 'total_amount')
    list_display_links = ('order', 'product')
    list_select_related = True
    ordering = ('order', 'product')


#@admin.register(Basket)
#class BasketAdmin(admin.ModelAdmin):
#    pass
