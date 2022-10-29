from django.db import models
from django.conf import settings

from accounts.models import Site_User
from products.models import Product

class Cart_Item(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default = 0)

    def __str__(self):
        return self.product.product_name

class Shopping_Cart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(Cart_Item)
    ordered = models.BooleanField(default=False)
    

    def get_total_price(self):
        return sum([item.product.price * item.quantity for item in self.items.all()])

    def get_cart_items(self):
        return self.items.all()
