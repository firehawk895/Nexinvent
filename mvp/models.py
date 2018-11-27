from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.db import models


class Supplier(models.Model):
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


class Product(models.Model):
    # Product table is not normalized for convenience
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    sku = models.CharField(max_length=256)
    unit = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    address = models.TextField(blank=True)
    phone_number = models.CharField(validators=[Supplier.phone_regex], max_length=17, blank=True)
    email = models.EmailField(max_length=70, blank=False)
    # Aggregated stats
    total_orders = models.IntegerField(default=0)
    total_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO: figure out automated count on a join table
    total_suppliers = models.IntegerField(default=0)
    total_inventory_items = models.IntegerField(default=0)


class AssociatedSupplier(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_pending_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    STATUSES = (
        ("submitted", "Submitted"),
        ("accepted", "Accepted"),
        ("in_transit", "In-Transit"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("checked_in", "Checked-In")
    )
    PAYMENT_STATUSES = (
        ("invoice_received", "Invoice received"),
        ("paid_full", "Paid (full)"),
        ("paid_partial", "Paid (partial)"),
        ("disputed", "Disputed"),
        ("due", "due")
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    # need to add a reference to employee id here who placed the order
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(choices=PAYMENT_STATUSES, max_length=18)
    status = models.CharField(choices=STATUSES, max_length=18)
    invoice_images = ArrayField(ArrayField(models.URLField()))
    requested_delivery_date = models.DateTimeField(null=True)
    delivered_on = models.DateTimeField(null=True)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2)
    comment = models.CharField(max_length=1024)


class OrderItems(models.Model):
    STATUSES = (
        ("missing", "Missing/Not Delivered"),
        ("received_full", "Received (Full)"),
        ("received_partial", "Received (Partial)"),
        ("returned", "Returned"),
        ("new", "New/Substitute"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, max_length=18)
    qty_received = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.TextField(blank=True)
    comment = models.CharField(max_length=1024)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    note = models.CharField(max_length=512)


class FavProducts(models.Model):
    # adding supplier for easy entry point, although not needed
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
