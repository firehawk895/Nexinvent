# Generated by Django 2.1.2 on 2019-06-23 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0004_auto_20190622_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='requested_delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
