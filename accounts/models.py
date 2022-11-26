from django.db import models
from django.conf import settings
from django.utils import timezone
from cities_light.models import City
from shopping_cart.models import Shopping_Cart
from django.shortcuts import reverse
#from shopping_cart.models import Shopping_Cart


# Create your models here.
class Site_User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
 #   cart = models.OneToOneField(Shopping_Cart)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    building_address = models.CharField(max_length=5)
    apartment_address = models.CharField(max_length = 10,blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=10)

class User_Address(models.Model):
    user = models.ForeignKey(Site_User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Order(models.Model):
<<<<<<< HEAD
    cart = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank = True, null=True)
    order_date = models.DateTimeField(default = timezone.now())
    phone = models.CharField(max_length=9)
    email = models.EmailField((""), max_length=254, blank=True)

    def get_absolute_url(self):
        return reverse("store:order-summary", kwargs={
            'id': self.cart.id
        })
=======
    cart = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=9, default="")
    email = models.EmailField(default = (""), max_length=254)
>>>>>>> main
    