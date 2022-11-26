<<<<<<< HEAD
# Generated by Django 4.1.3 on 2022-11-21 14:17

import datetime
=======
# Generated by Django 4.1.3 on 2022-11-26 14:48

>>>>>>> main
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0005_alter_cart_item_product_alter_cart_item_user'),
        ('accounts', '0005_alter_address_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping_cart.shopping_cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
<<<<<<< HEAD
            field=models.EmailField(blank=True, max_length=254, verbose_name=''),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 21, 14, 17, 15, 942506, tzinfo=datetime.timezone.utc)),
=======
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
>>>>>>> main
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=9),
            preserve_default=False,
        ),
    ]
