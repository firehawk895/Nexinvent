from rest_framework import serializers

from .models import Order


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
                  'has_comment', 'is_disputed')
