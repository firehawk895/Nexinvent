from django.db import models, transaction
from django.db.models import Sum


class CartManager(models.Manager):
    def remove_supplier_cart(self, restaurant, supplier):
        return self.get_queryset().filter(supplier=supplier, restaurant=restaurant).delete()


class OrderManager(models.Manager):
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
