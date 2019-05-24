from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator

from .models import Order, Product, OrderItem, Restaurant, Cart, Supplier


class OrderSerializer(serializers.ModelSerializer):
    has_comment = serializers.SerializerMethodField()
    is_disputed = serializers.SerializerMethodField()
    supplier_name = serializers.SerializerMethodField()

    def get_has_comment(self, obj):
        return True if obj.comment else False

    def get_is_disputed(self, obj):
        return True if obj.payment_status == Order.DISPUTED else False

    def get_supplier_name(self, obj):
        return obj.supplier.name

    class Meta:
        model = Order
        fields = ('status', 'id', 'supplier', 'supplier_name', 'created_at', 'requested_delivery_date', 'amount', 'invoice_no',
                  'has_comment', 'is_disputed', 'restaurant')
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'supplier', 'name', 'sku', 'unit', 'description', 'price')

        depth = 1


class CartItemSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(required=True)

    def validate(self, attrs):
        """
        We are using optimistic deletes in the front end. There could be a case where the page is stale,
        hence make sure the backend cart is the same as the front end cart. Also this is a great place to calculate the
        total amount
        :param attrs:
        :return:
        """
        #
        # There could be a case where the page is stale, hence make sure the backend cart is the same as the front end
        # cart.

        # funny thing, the serializer sends you the objects lulz.
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
        print(validated_data)
        req_dd = validated_data["req_dd"] if "req_dd" in validated_data else None
        order = Order.objects.create(supplier=validated_data["supplier"], restaurant=validated_data["restaurant"],
                             amount=validated_data["total"],status=Order.SUBMITTED,
                                     requested_delivery_date=req_dd)
        for cart_item in validated_data["cart_items"]:
            OrderItem.objects.create(order=order, quantity=cart_item["quantity"],
                                     product=cart_item["product"], amount=cart_item["total"])
            cart_obj = cart_item["id"]
            cart_obj.delete()


# explicitly specify the querysets so that they can be used for POST API as NON read only
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


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('order', 'status', 'quantity', 'qty_received', 'product', 'amount', 'note', 'comment')
        depth = 1
