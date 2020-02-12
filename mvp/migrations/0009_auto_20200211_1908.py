# Generated by Django 2.1.2 on 2020-02-11 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0008_slugify_20191213_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='whatsapp_status',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('In-Transit', 'In-Transit'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Checked-In', 'Checked-In')], max_length=18),
        ),
    ]
