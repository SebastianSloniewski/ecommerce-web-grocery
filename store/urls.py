from itertools import product
from django.urls import path, include

app_name = 'store'

urlpatterns = [
 path('products/', include('products.urls'), name='products')   
]