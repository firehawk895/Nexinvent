from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.renderers import JSONRenderer

from .models import Order, Product, OrderItem, Restaurant


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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('supplier', 'name', 'sku', 'unit', 'description', 'price')


# class OrderItemSerializer(serializers.ModelSerializer):
#     order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
#
#     class Meta:
#         model = OrderItem
#         fields = ('order', 'product', 'quantity', 'note', 'comment')
#
#
# class OrderNewSerializer(serializers.ModelSerializer):
#     order_items = OrderItemSerializer(many=True)
#
#     def create(self, validated_data):
#         return Order.objects.create(validated_data, Restaurant.objects.first().id, None)
#
#     # need to implement:
#     # def update(self, instance, validated_data): if you want to support updation
#
#     class Meta:
#         model = Order
#         fields = ('supplier', 'requested_delivery_date', 'comment', 'order_items')

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)

    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity', 'total')


class OrderNewSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        return Order.objects.create(validated_data, Restaurant.objects.first().id, None)

    class Meta:
        model = Order
        fields = ('supplier', 'requested_delivery_date', 'comment', 'order_items')
