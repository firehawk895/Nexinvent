# Generated by Django 2.1.2 on 2019-05-23 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0020_auto_20190515_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
