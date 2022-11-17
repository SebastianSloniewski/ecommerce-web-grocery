from django.db import models
from django.conf import settings

from accounts.models import Site_User
from products.models import Product

class Cart_Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  blank=True, null = True)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

    def get_total_item_price(self):
        return self.quantity * self.product.base_price

class Shopping_Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(Cart_Item)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
      return f'{self.user.username}, {"".join(item.product.product_name for item in self.items.all())}' 

    def get_total_price(self):
        return sum([item.product.base_price * item.quantity for item in self.items.all()])

    def get_cart_items(self):
        return self.items.all()
