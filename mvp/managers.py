from django.contrib.auth.models import User
from django.db import models


class OrderManager(models.Manager):
    def create(self, order, restaurant_id, employee_id):
        """
        Model manager encapsulating the send all orders logic
        :param data:
        No, data is actually:
        {
                "delivery_charge": 0,
                "reqDD": null,
                "comment": null,
                "supplier_id": "26837724",
                "products": [{
                    "product_id": "26837749",
                    "quantity": 1,
                    "supplier_id": "26837724",
                    "price": 98
                }, {
                    "product_id": "26837753",
                    "quantity": 1,
                    "supplier_id": "26837724",
                    "price": 165
                }]
            }]
        }
        which is part of the bigger picture:
        {
            "data": [{
                "reqDD": null,
                "comment": null,
                "supplier_id": "26836656",
                "products": [{
                    "product_id": "26836661",
                    "quantity": 3,
                    "supplier_id": "26836656",
                    "price": 788
                }]
            }, {
                "delivery_charge": 0,
                "reqDD": null,
                "comment": null,
                "supplier_id": "26837724",
                "products": [{
                    "product_id": "26837749",
                    "quantity": 1,
                    "supplier_id": "26837724",
                    "price": 98
                }, {
                    "product_id": "26837753",
                    "quantity": 1,
                    "supplier_id": "26837724",
                    "price": 165
                }]
            }]
        }
        :return:
        """
        from .models import Order, OrderItem
        from .models import Supplier, Restaurant
        print(order)

        new_order = Order(
            supplier_id=order.get('supplier').id,
            restaurant_id=Restaurant.objects.first().id,
            amount=sum(map(lambda x: x["total"], order.get("order_items"))),
            employee_id=User.objects.first().id,
            status=Order.SUBMITTED,
            requested_delivery_date=None,
            comment="What a comment"
        )
        new_order.save()
        for order_item in order.get("order_items"):
            new_order_item = OrderItem(
                order=new_order,
                quantity=order_item.get("quantity"),
                product_id=order_item.get("product").id,
                total=order_item.get("total"),
                note=order_item.get("note", ""),
                comment=order_item.get("comment", "")
            )
            new_order_item.save()
        return new_order
