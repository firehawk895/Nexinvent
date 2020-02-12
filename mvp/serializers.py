from django.utils import timezone
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator

from mvp.notifyers import send_whatsapp_notifications
from .models import Order, Product, OrderItem, Restaurant, Cart, Supplier


class OrderSerializer(serializers.ModelSerializer):
    # has_comment = serializers.SerializerMethodField()
    # is_disputed = serializers.SerializerMethodField()

    def get_has_comment(self, obj):
        return True if obj.comment else False

    def get_is_disputed(self, obj):
        return True if obj.payment_status == Order.DISPUTED else False

    class Meta:
        model = Order
        fields = ('status', 'id', 'supplier', 'created_at', 'requested_delivery_date', 'amount',
                  'invoice_no', 'restaurant', 'amount_checked_in', 'whatsapp_status')
        depth = 1


# You definitely need a patch serializer to maintain integrity
class OrderSerializerPatch(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('payment_status', 'invoice_no', 'status')

    def update(self, instance, validated_data):
        # record the old instance status
        old_status = instance.status
        super().update(instance, validated_data)
        # send a notification only when status changes and a status change has been explicitly
        # sent in the the patch request
        if instance.status != old_status and "status" in validated_data:
            send_whatsapp_notifications(instance)
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'status', 'quantity', 'qty_received', 'product', 'amount', 'note', 'comment', 'created_at', 'modified_at')
        depth = 1


class OrderInstanceSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('status', 'id', 'supplier', 'created_at', 'requested_delivery_date', 'amount', 'amount_checked_in',
                  'invoice_no', 'order_items', 'restaurant', 'checked_in_at', 'payment_status', 'delivered_on')
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'supplier', 'name', 'sku', 'unit', 'description', 'price')

        depth = 1


class CartItemSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.DecimalField(required=True, decimal_places=2, max_digits=10)

    def validate(self, attrs):
        """
        We are using optimistic deletes in the front end. There could be a case where the page is stale,
        hence make sure the backend cart is the same as the front end cart. Also this is a great place to calculate the
        total amount
        :param attrs:
        :return:
        """

        # funny thing, the serializer sends you the objects.
        cart_object = attrs["id"]
        product_obj = attrs["product"]
        cart_item = Cart.objects.get(pk=cart_object.id)
        if cart_item.product.id != product_obj.id or cart_item.quantity != attrs["quantity"]:
            raise serializers.ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: "Please refresh the page before sending orders"})
        # inject the sub total
        attrs["total"] = product_obj.price * attrs["quantity"]
        return attrs


class SendOrderSerializer(serializers.Serializer):
    # TODO: You can change the queryset to only the associated suppliers for security/integrity
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    req_dd = serializers.DateField(required=False)
    cart_items = CartItemSerializer(many=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    def validate(self, attrs):
        """
        Don't need extra validation; great place to calculate the grand total
        :param attrs:
        :return:
        """
        # inject the total
        attrs["total"] = sum(map(lambda x: x["total"], attrs["cart_items"]))
        return attrs

    # The default implementation for multiple object creation using ListSerializer is to simply call .create()
    # for each item in the list, hence lets override create
    def create(self, validated_data):
        # don't want to move this logic to a model manager
        # drf did so much hard work in getting all the cart objects, why query them again for a delete?
        req_dd = validated_data["req_dd"] if "req_dd" in validated_data else None
        order = Order.objects.create(supplier=validated_data["supplier"], restaurant=validated_data["restaurant"],
                             amount=validated_data["total"],status=Order.SUBMITTED,
                                     requested_delivery_date=req_dd)

        for cart_item in validated_data["cart_items"]:
            OrderItem.objects.create(order=order, quantity=cart_item["quantity"],
                                     product=cart_item["product"], amount=cart_item["total"])
            cart_obj = cart_item["id"]
            cart_obj.delete()

        # warning: possible atomic transaction rollback even though message/email is sent
        send_whatsapp_notifications(order)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'supplier', 'product', 'restaurant', 'quantity', 'note')
        depth = 1
        # Only for POST, don't allow a duplicate cart item
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('supplier', 'product', 'restaurant'),
                message="Item is already in cart, try refreshing the page."
            )
        ]

    def validate_quantity(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity cannot be 0")
        return value


class OrderItemCheckinSerializer(serializers.Serializer):
    # TODO: I would love it if this queryset could be restricted to 1 order
    id = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all())
    status = serializers.ChoiceField(OrderItem.STATUSES)
    qty_received = serializers.DecimalField(decimal_places=2, max_digits=10)

    def validate(self, attrs):
        """
        Check if status syncs with qty_received
        :param attrs:
        :return:
        """
        # TODO: for more stronger entity add a check for "New" status items
        order_item = attrs["id"]
        if (((attrs["status"] == OrderItem.MISSING or attrs["status"] == OrderItem.RETURNED) and attrs["qty_received"] != 0.00) or
            (attrs["status"] == OrderItem.RECEIVED and attrs["qty_received"] < order_item.quantity) or
            (attrs["status"] == OrderItem.RECEIVED_PARTIAL and (attrs["qty_received"] == 0 or attrs["qty_received"] >= order_item.quantity))):
            raise serializers.ValidationError("Status and Received Quantity do not match.")
        return attrs


class CheckinSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    delivered_on = serializers.DateField(allow_null=True)
    invoice_no = serializers.CharField(max_length=256, allow_blank=True)
    order_items = OrderItemCheckinSerializer(many=True)

    def validate(self, attrs):
        order_obj = attrs["order"]
        if order_obj.status == Order.DELIVERED:
            raise serializers.ValidationError("A finalized order cannot be checked in again")
        return attrs

    def save(self, **kwargs):
        order_obj = self.validated_data["order"]
        order_obj.status = Order.CHECKED_IN
        if "delivered_on" in self.validated_data:
            order_obj.delivered_on = self.validated_data["delivered_on"]
        order_obj.invoice_no = self.validated_data["invoice_no"]

        amount_checked_in = 0
        for order_item in self.validated_data["order_items"]:
            order_item_obj = order_item["id"]
            order_item_obj.status = order_item["status"]
            order_item_obj.qty_received = order_item["qty_received"]
            amount_checked_in += order_item_obj.product.price * order_item_obj.qty_received
            order_item_obj.save()

        order_obj.amount_checked_in = amount_checked_in
        order_obj.save()
        send_whatsapp_notifications(order_obj)


class CartSerializerPost(CartSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())


# lets not allow modification of supplier, product and restaurant
class CartSerializerPatch(CartSerializer):
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)


# Using this for deleting cart items based on supplier id
class CartSerializerDeleteSupplierWise(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    supplier_list = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all()))

    def perform_delete(self):
        for supplier in self.validated_data["supplier_list"]:
            Cart.objects.remove_supplier_cart(self.validated_data["restaurant"], supplier)


class TwilioStatusCallBackSerializer(serializers.Serializer):
    """
    Twilio posts with the following known info:
    {
        "sid": "SM4262411b90e5464b98a4f66a49c57a97",
        "date_created": "Wed, 07 Feb 2018 17:46:52 +0000",
        "date_updated": "Wed, 07 Feb 2018 17:46:52 +0000",
        "date_sent": null,
        "account_sid": "AC0db966d80e9f1662da09c61287f8bba1",
        "to": "+15622089096",
        "from": null,
        "messaging_service_sid": "MG4d9d720b38f7892254869fabdca51e69",
        "body": "Test",
        "status": "accepted",
        "num_segments": "0",
        "num_media": "0",
        "direction": "outbound-api",
        "api_version": "2010-04-01",
        "price": null,
        "price_unit": null,
        "error_code": null,
        "error_message": null,
        "uri": "/2010-04-01/Accounts/AC0db966d80e9f1662da09c61287f8bba1/Messages/SM4262411b90e5464b98a4f66a49c57a97.json",
        "subresource_uris": {
            "media": "/2010-04-01/Accounts/AC0db966d80e9f1662da09c61287f8bba1/Messages/SM4262411b90e5464b98a4f66a49c57a97/Media.json"
        }
    }
    Source: https://www.twilio.com/docs/sms/outbound-message-logging

    The serializer field would have been
    date_created = serializers.CharField(allow_blank=False)

    The validator for this field would have been:
    def validate_date_created(self, value):
        # API comes with unnecessary quotes that need to be stripped before conversion
        # format source - https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        # iso8601 - https://docs.python.org/2/library/datetime.html#datetime.date.isoformat
        return datetime.strptime(value.strip("\""), "%a, %d %b %Y %H:%M:%S %z")

    But after hitting the API, this is the actual info twilio is sending:
    {
        'EventType': 'DELIVERED',
        'SmsSid': 'SM86443ea315c64efc8c0bf852915593ae',
        'SmsStatus': 'delivered',
        'MessageStatus': 'delivered',
        'ChannelToAddress': '+919643713143',
        'To': 'whatsapp:+919643713143',
        'ChannelPrefix': 'whatsapp',
        'MessageSid': 'SM86443ea315c64efc8c0bf852915593ae',
        'AccountSid': 'AC0358dd1e2e26a0f0a98a3b52532d9ae2',
        'From': 'whatsapp:+18443112326',
        'ApiVersion': '2010-04-01',
        'ChannelInstallSid': 'XE6b1386f816ea573d2a23dfc8dc2f1dbb'
    }
    """
    MessageStatus = serializers.CharField(allow_blank=False)
    # TODO: Someday make the saving generic by taking model name and primary key or fire an event
    # the order id
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    def save(self, **kwargs):
        d = self.validated_data

        order = d["order_id"]
        order.whatsapp_status = d["MessageStatus"]
        # unfortunately there is no timestamp from twilio, so adding a close estimation
        order.whatsapp_timestamp = timezone.now()
        order.save()

