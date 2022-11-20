from django.db import models
from django.conf import settings
import operator
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

    def save(self, *args, **kwargs):
        self.items = sorted(self.items, key=operator.attrgetter('product.product_name'))
        super(Product, self).save(*args, **kwargs) # Call the "real" save() method.


    def get_total_price(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.product.price
        return total

    def get_cart_items(self):
        return self.items.all()

    def items_count(self):
        total=0
        for item in self.items.all():
            total += 1
        return total
