from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from products.views import(
    shop_view, 
    ProductDetailView
)
from shopping_cart.views import(
    ShoppingCartSummaryView,
    remove_single_item,
    add_to_cart, 
    remove_from_cart, 
) 
from .views import(
    index_view,
    CheckoutView
)

app_name = 'store'

urlpatterns = [
 path('',index_view, name='index'),
 path('shop-grid/', shop_view ,name='shop-grid'),
 path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-details'),
 path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
 path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
 path('cart-summary/', ShoppingCartSummaryView.as_view(), name='cart-summary'),
 path('remove-item-from-cart/<slug>', remove_single_item, name="remove-single-item"),
 path('checkout/', CheckoutView.as_view(),name='checkout')
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
