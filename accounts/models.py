from django.db import models
from django.conf import settings
from cities_light.models import City
from shopping_cart.models import Shopping_Cart
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
    apartment_address = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class User_Address(models.Model):
    user = models.ForeignKey(Site_User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Order(models.Model):
    cart = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField()
    phone = models.CharField(max_length=9)
    email = models.EmailField((""), max_length=254)
    