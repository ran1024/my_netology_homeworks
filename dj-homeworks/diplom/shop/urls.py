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
from .views import main_page, show_category, product_detail, customer_login, customer_logout


urlpatterns = [
    path('', main_page, name='main_page'),
    path('category/<str:id>/<str:brand_id>/', show_category, name='show_category'),
    path('product/<str:product_id>/', product_detail, name='product_detail'),
    path('customer_login/', customer_login, name='customer_login'),
    path('customer_logout/', customer_logout, name='customer_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
