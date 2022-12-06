# Generated by Django 2.2.14 on 2022-12-06 14:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100)),
                ('building_address', models.CharField(max_length=5)),
                ('apartment_address', models.CharField(blank=True, max_length=10, null=True)),
                ('postal_code', models.CharField(max_length=10)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_image', models.ImageField(upload_to='')),
                ('category_name', models.CharField(max_length=50)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Shopping_Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='store.Cart_Item')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_description', models.CharField(blank=True, max_length=400)),
                ('product_image', models.ImageField(upload_to='')),
                ('base_price', models.FloatField()),
                ('discount', models.IntegerField(default=0)),
                ('price', models.FloatField(default=models.FloatField())),
                ('slug', models.SlugField(default=models.CharField(max_length=50))),
                ('featured', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(default=datetime.datetime(2022, 12, 6, 14, 48, 7, 632107, tzinfo=utc))),
                ('phone', models.CharField(max_length=9)),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Address')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.Shopping_Cart')),
            ],
        ),
        migrations.AddField(
            model_name='cart_item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product'),
        ),
    ]
