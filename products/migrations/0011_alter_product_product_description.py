# Generated by Django 4.1.3 on 2022-11-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
