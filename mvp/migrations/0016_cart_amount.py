# Generated by Django 2.1.2 on 2018-12-27 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0015_cart_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]