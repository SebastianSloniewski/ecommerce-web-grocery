from django.db import models

#from shopping_cart.models import Shopping_Cart


# Create your models here.
class Site_User(models.Model):
    email = models.CharField(max_length = 20)
    phone_number = models.CharField(default = "", max_length=9)
 #   cart = models.OneToOneField(Shopping_Cart)