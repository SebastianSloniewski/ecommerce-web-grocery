from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from products.models import Product
from products.views import basic_view, add_to_cart, remove_from_cart, ProductDetailView
from .views import index_view

app_name = 'store'

urlpatterns = [
 path('',index_view, name='index'),
 path('shop-grid/', basic_view ,name='shop-grid'),
 path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-details'),
 path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
 path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart')
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
