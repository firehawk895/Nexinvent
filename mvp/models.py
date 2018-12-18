from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.db import models

from utility.behaviours import TimeStampable


class Supplier(TimeStampable, models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=256)
    min_order = models.IntegerField(default=0)
    sales_rep = models.CharField(max_length=256)
    address = models.TextField(blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    email = models.EmailField(max_length=70, blank=False)
    # TODO: add a gst no validator here
    gst_no = models.CharField(max_length=256)


class Product(TimeStampable, models.Model):
    # Product table is not normalized for convenience
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=256)
    sku = models.CharField(max_length=256)
    unit = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Restaurant(TimeStampable, models.Model):
    fav_products = models.ManyToManyField(Product, blank=True)
    name = models.CharField(max_length=256)
    address = models.TextField(blank=True)
    phone_number = models.CharField(validators=[Supplier.phone_regex], max_length=17, blank=True)
    email = models.EmailField(max_length=70, blank=False)
    # Aggregated stats
    total_orders = models.IntegerField(default=0)
    total_order_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    # TODO: figure out automated count on a join table
    total_suppliers = models.IntegerField(default=0)
    total_inventory_items = models.IntegerField(default=0)
    associated_suppliers = models.ManyToManyField(Supplier, through='AssociatedSupplier')


class AssociatedSupplier(TimeStampable, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_pending_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order(TimeStampable, models.Model):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    CHECKED_IN = "checked_in"

    STATUSES = (
        (SUBMITTED, "Submitted"),
        (ACCEPTED, "Accepted"),
        (IN_TRANSIT, "In-Transit"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
        (CHECKED_IN, "Checked-In")
    )
    INVOICE_RECEIVED = "invoice_received"
    PAID_FULL = "paid_full"
    PAID_PARTIAL = "paid_partial"
    DISPUTED = "disputed"
    DUE = "due"

    PAYMENT_STATUSES = (
        (INVOICE_RECEIVED, "Invoice received"),
        (PAID_FULL, "Paid (full)"),
        (PAID_PARTIAL, "Paid (partial)"),
        (DISPUTED, "Disputed"),
        ("due", "due")
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(choices=PAYMENT_STATUSES, max_length=18, blank=True, null=True)
    status = models.CharField(choices=STATUSES, max_length=18)
    invoice_images = ArrayField(ArrayField(models.URLField()), blank=True, null=True)
    requested_delivery_date = models.DateTimeField(blank=True, null=True)
    delivered_on = models.DateTimeField(blank=True, null=True)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    comment = models.CharField(max_length=1024, blank=True)
    invoice_no = models.CharField(max_length=256, blank=True)


class OrderItem(TimeStampable, models.Model):
    STATUSES = (
        ("missing", "Missing/Not Delivered"),
        ("received_full", "Received (Full)"),
        ("received_partial", "Received (Partial)"),
        ("returned", "Returned"),
        ("new", "New/Substitute"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    status = models.CharField(choices=STATUSES, max_length=18)
    qty_received = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.TextField(blank=True)
    comment = models.CharField(max_length=1024)


class Cart(TimeStampable, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    note = models.CharField(max_length=512)

# Dont need this anymore, using a standard Many to Many relationship of restaurants vs fav_products
# class FavProducts(TimeStampable, models.Model):
#     # adding supplier for easy entry point, although not needed
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='fav_products')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
