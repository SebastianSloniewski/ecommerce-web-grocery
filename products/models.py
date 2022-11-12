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
    discount = models.IntegerField(blank = True, null = True)
    slug = models.SlugField(default = product_name)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("store:product-details", kwargs={
            'slug': self.slug
        })
    
