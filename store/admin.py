from itertools import product
from django.contrib import admin
from .models import(
    Product,
    Category,
    Shopping_Cart,
    Cart_Item
)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shopping_Cart)
admin.site.register(Cart_Item)