from django.urls import path

from .views import cart_add, cart_remove, cart_detail, cart_clear

app_name = 'cart'

urlpatterns = [
    path('remove/<str:product_id>/', cart_remove, name='cart_remove'),
    path('add/<str:product_id>/', cart_add, name='cart_add'),
    path('', cart_detail, name='cart_detail'),
    path('clear/', cart_clear, name='cart_clear'),
]
