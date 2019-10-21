# Generated by Django 2.1.2 on 2019-06-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0003_auto_20190617_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(blank=True, choices=[('Missing/Not Delivered', 'Missing/Not Delivered'), ('Received (Full)', 'Received (Full)'), ('Received (Partial)', 'Received (Partial)'), ('Returned', 'Returned'), ('New', 'New')], max_length=50),
        ),
    ]