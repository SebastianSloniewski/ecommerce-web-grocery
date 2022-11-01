from django.urls import path
from .views import product_list, ShopView

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product-list')
]