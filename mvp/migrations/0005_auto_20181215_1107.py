# Generated by Django 2.1.2 on 2018-12-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0004_auto_20181215_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='fav_products',
            field=models.ManyToManyField(blank=True, to='mvp.Product'),
        ),
    ]
