from django.contrib import admin
from .models import Orders, ProductsInOrder


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    fields = ('product', 'number_of_units', 'price_of_unit', 'total_amount')
    readonly_fields = ('product', 'price_of_unit', 'total_amount')
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
    fields = (('status', 'customer'), 'total_number', 'total_price', 'comments', ('created', 'updated'))
    readonly_fields = ('customer', 'total_number', 'total_price', 'comments', 'created', 'updated')
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
