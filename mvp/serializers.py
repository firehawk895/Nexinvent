from rest_framework import serializers
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


class OrderNewSerializer(serializers.Serializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    requested_delivery_date = serializers.DateField(required=False)
    note = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return Order.objects.create_new_order(validated_data["supplier_id"], validated_data.get("requested_delivery_date"),
                                              validated_data.get("note"), self.context.restaurant_id)

    class Meta:
        fields = ('supplier', 'requested_delivery_date', 'note')


# explicitly specify the querysets so that they can be used for POST API as NON read only
class CartSerializer(serializers.ModelSerializer):
    def validate_quantity(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity cannot be 0")

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


class CartSerializerPost(CartSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())


# lets not allow modification of supplier, product and restaurant
class CartSerializerPatch(CartSerializer):
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('order', 'status', 'quantity', 'qty_received', 'product', 'amount', 'note', 'comment')
        depth = 1
