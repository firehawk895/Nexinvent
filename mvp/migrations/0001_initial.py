# Generated by Django 2.1.2 on 2018-12-15 07:19

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssociatedSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_pending_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('note', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='FavProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_status', models.CharField(choices=[('invoice_received', 'Invoice received'), ('paid_full', 'Paid (full)'), ('paid_partial', 'Paid (partial)'), ('disputed', 'Disputed'), ('due', 'due')], max_length=18)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('accepted', 'Accepted'), ('in_transit', 'In-Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ('checked_in', 'Checked-In')], max_length=18)),
                ('invoice_images', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=None), size=None)),
                ('requested_delivery_date', models.DateTimeField(null=True)),
                ('delivered_on', models.DateTimeField(null=True)),
                ('delivery_charge', models.DecimalField(decimal_places=2, max_digits=6)),
                ('comment', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('missing', 'Missing/Not Delivered'), ('received_full', 'Received (Full)'), ('received_partial', 'Received (Partial)'), ('returned', 'Returned'), ('new', 'New/Substitute')], max_length=18)),
                ('qty_received', models.IntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('note', models.TextField(blank=True)),
                ('comment', models.CharField(max_length=1024)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('sku', models.CharField(max_length=256)),
                ('unit', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=70)),
                ('total_orders', models.IntegerField(default=0)),
                ('total_order_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_suppliers', models.IntegerField(default=0)),
                ('total_inventory_items', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('min_order', models.IntegerField(default=0)),
                ('sales_rep', models.CharField(max_length=256)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=70)),
                ('gst_no', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Supplier'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Restaurant'),
        ),
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Supplier'),
        ),
        migrations.AddField(
            model_name='favproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Product'),
        ),
        migrations.AddField(
            model_name='favproducts',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Restaurant'),
        ),
        migrations.AddField(
            model_name='favproducts',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Supplier'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Restaurant'),
        ),
        migrations.AddField(
            model_name='associatedsupplier',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Restaurant'),
        ),
        migrations.AddField(
            model_name='associatedsupplier',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Supplier'),
        ),
    ]
