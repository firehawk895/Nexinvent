from django.db import models, transaction
from django.db.models import Sum


class CartManager(models.Manager):
    def remove_supplier_cart(self, supplier_id, restaurant_id):
        return CartManager.objects.delete(supplier_id=supplier_id, restaurant_id=restaurant_id)


class OrderManager(models.Manager):
    @transaction.atomic
    def create_new_order(self, supplier_id, req_dd, comment, restaurant_id):
        """

        :param supplier_id:
        :param req_dd:
        :param comment:
        :param restaurant_id:
        :return:
        """
        from .models import Cart, Order, OrderItem
        cart_items = Cart.objects.filter(restaurant_id=restaurant_id, supplier_id=supplier_id)
        amount = sum(map(lambda x: x.amount, cart_items))
        order = Order.objects.save(supplier_id=supplier_id, restaurant_id=restaurant_id, amount=amount,
                             status=Order.SUBMITTED, requested_delivery_date=req_dd, comment=comment)
        for c in cart_items:
            OrderItem.objects.save(order=order, quantity=c.quantity, product=c.product, amount=c.amount, note=c.note)
        cart_items.delete()

    def get_order_aggregates(self, restaurant_id):
        """
        get a few aggregate values for the order history screen
        :param restaurant_id:
        :return:
        """
        from .models import Order, AssociatedSupplier, Product
        assoc_suppliers = AssociatedSupplier.objects.filter(restaurant_id=restaurant_id)
        return {
            "total_orders": Order.objects.filter(restaurant_id=restaurant_id).count(),
            "total_order_value": Order.objects.filter(restaurant_id=restaurant_id).aggregate(
                total_order_value=Sum('amount'))["total_order_value"],
            "total_suppliers": assoc_suppliers.count(),
            "total_inventory_items": Product.objects.filter(supplier_id__in=map(
                lambda x: x.supplier_id, assoc_suppliers)).count()
        }
