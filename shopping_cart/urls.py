from django.urls import path
from .views import ShoppingCartSummaryView

app_name = 'cart'

urlpatterns = [
    path('cart-summary/', ShoppingCartSummaryView.as_view(), name='cart-summary')
]