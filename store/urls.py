from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from products.views import basic_view
from .import views

app_name = 'store'

urlpatterns = [
 path('', views.index_view, name='index'),  
 path('shop-grid/', basic_view ,name='shop-grid')
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
