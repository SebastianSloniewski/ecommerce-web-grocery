from django.db import models

# Create your models here.
class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE)
    category_name = models.CharField(max_length = 50)

class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 50)
    product_description = models.CharField(max_length = 400)
    product_image = models.ImageField()
    price = models.IntegerField()