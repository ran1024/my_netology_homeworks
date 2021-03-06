"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import main_page, show_category, ProductDetailView, response_add, customer_logout, CustomerLoginView

urlpatterns = [
    path('', main_page, name='main_page'),
    path('category/<str:category_id>/<str:brand_id>/', show_category, name='show_category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('response/<str:product_id>/', response_add, name='response_add'),
    path('customer_login/', CustomerLoginView.as_view(), name='customer_login'),
    path('customer_logout/', customer_logout, name='customer_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
