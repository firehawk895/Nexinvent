# Generated by Django 2.1.2 on 2018-12-27 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0016_cart_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='qty',
            new_name='quantity',
        ),
    ]