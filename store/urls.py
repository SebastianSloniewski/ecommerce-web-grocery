
from django.urls import path, include


app_name = 'store'

urlpatterns = [
 path('', 'index.html', name=home)
 path('products/', include('products.urls'), name='products'),  
 path('cart/', include('shopping_cart.urls'), name='cart') 
]