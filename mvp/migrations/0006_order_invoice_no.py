# Generated by Django 2.1.2 on 2018-12-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0005_auto_20181215_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_no',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
    ]