
from django.urls import path, include
from .import views

app_name = 'store'

urlpatterns = [
 path('', views.index_view, name='index'),  
 path('products/', include('products.urls'), name='products'),  
 path('cart/', include('shopping_cart.urls'), name='cart') 
]