from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.category_name


        

class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 50)
    product_description = models.CharField(max_length = 400)
    product_image = models.ImageField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    discount_price = models.FloatField(default=0) 
    slug = models.SlugField(blank = True, null = True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.discount_price = (self.price * (100 - self.discount) / 100)

    def get_absolute_url(self):
        return reverse("store:product-details", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            'slug': self.slug
        })
