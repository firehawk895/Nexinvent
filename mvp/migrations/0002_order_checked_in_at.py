# Generated by Django 2.1.2 on 2019-05-31 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checked_in_at',
            field=models.DateTimeField(null=True),
        ),
    ]