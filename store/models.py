from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from cities_light.models import City
from products.models import Product

class Category(models.Model):
    category_image = models.ImageField()
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.category_name


        

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 50)
    product_description = models.CharField(max_length = 400, blank=True)
    product_image = models.ImageField()
    base_price = models.FloatField()
    discount = models.IntegerField(default=0)
    price = models.FloatField(default = base_price, blank=True) 
    slug = models.SlugField(blank = True, null = True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.price = (self.base_price * (100 - self.discount) / 100)
        self.price = round(self.price,2)
        super(Product, self).save(*args, **kwargs) # Call the "real" save() method.


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
    def get_price(self):
        return "{:.2f}".format(self.price)


class Cart_Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  blank=True, null = True)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

    def get_total_item_price(self):
        return "{:.2f}".format(self.quantity * self.product.price)

        

class Shopping_Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(Cart_Item)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
      return f'{self.user.username}, {"".join(item.product.product_name for item in self.items.all())}' 


    def get_total_price(self):
        total = 0
        for cart_item in self.items.all():
            total += (cart_item.product.price * cart_item.quantity)
        return "{:.2f}".format(total)

    def get_cart_items(self):
        return self.items.all()

    def items_count(self):
        total=0
        for item in self.items.all():
            total += 1
        return total

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
    cart = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank = True, null=True)
    order_date = models.DateTimeField(default = timezone.now())
    phone = models.CharField(max_length=9)
    email = models.EmailField((""), max_length=254, blank=True)

    def get_absolute_url(self):
        return reverse("store:order-summary", kwargs={
            'id': self.cart.id
        })

    












