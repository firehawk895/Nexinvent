from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from utility.behaviours import TimeStampable

from .managers import OrderManager, CartManager


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

    def __str__(self):
        return self.name


class Product(TimeStampable, models.Model):
    # Product table is not normalized for convenience
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=256)
    sku = models.CharField(max_length=256)
    unit = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.supplier.name + " - " + self.name


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

    def __str__(self):
        return self.name


class AssociatedSupplier(TimeStampable, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_pending_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order(TimeStampable, models.Model):
    objects = OrderManager()

    SUBMITTED = "Submitted"
    ACCEPTED = "Accepted"
    IN_TRANSIT = "In-Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    CHECKED_IN = "Checked-In"

    STATUSES = (
        (SUBMITTED, "Submitted"),
        (ACCEPTED, "Accepted"),
        (IN_TRANSIT, "In-Transit"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
        (CHECKED_IN, "Checked-In")
    )
    INVOICE_RECEIVED = "Invoice received"
    PAID_FULL = "Paid (full)"
    PAID_PARTIAL = "Paid (partial)"
    DISPUTED = "Disputed"
    DUE = "due"

    PAYMENT_STATUSES = (
        (INVOICE_RECEIVED, "Invoice received"),
        (PAID_FULL, "Paid (full)"),
        (PAID_PARTIAL, "Paid (partial)"),
        (DISPUTED, "Disputed"),
        (DUE, "due")
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_checked_in = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_status = models.CharField(choices=PAYMENT_STATUSES, max_length=18, blank=True, null=True)
    status = models.CharField(choices=STATUSES, max_length=18)
    invoice_images = ArrayField(ArrayField(models.URLField()), blank=True, null=True)
    requested_delivery_date = models.DateField(blank=True, null=True)
    delivered_on = models.DateField(blank=True, null=True)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    comment = models.CharField(max_length=1024, blank=True)
    invoice_no = models.CharField(max_length=256, blank=True)
    checked_in_at = models.DateTimeField(null=True)


class OrderItem(TimeStampable, models.Model):
    MISSING = "Missing/Not Delivered"
    RECEIVED = "Received (Full)"
    RECEIVED_PARTIAL = "Received (Partial)"
    RETURNED = "Returned"
    NEW = "New"

    STATUSES = (
        (MISSING, "Missing/Not Delivered"),
        (RECEIVED, "Received (Full)"),
        (RECEIVED_PARTIAL, "Received (Partial)"),
        (RETURNED, "Returned"),
        (NEW, "New"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    status = models.CharField(choices=STATUSES, max_length=50, blank=True)
    quantity = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    qty_received = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.TextField(blank=True)
    comment = models.CharField(max_length=1024, blank=True)


class Cart(TimeStampable, models.Model):
    objects = CartManager()
    # adding a denormalized field to avoid joins and increase convenience
    # the convenience is very high when noticed in the front end
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    note = models.CharField(max_length=512, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

