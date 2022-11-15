# Generated by Django 4.1 on 2022-11-13 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_discount_product_slug_and_more'),
        ('shopping_cart', '0002_rename_owner_shopping_cart_user_cart_item_ordered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]