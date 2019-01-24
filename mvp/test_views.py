from django_dynamic_fixture import G
from rest_framework.test import APITestCase

from utility.generics_for_tests import TestCaseMixin

from .models import Supplier, Product, Restaurant, Cart, Order


class SendOrdersTestCase(APITestCase, TestCaseMixin):
    def setUp(self):
        import ipdb
        ipdb.set_trace()
        self.suppliers = [G(Supplier), G(Supplier)]
        products0 = [G(Product, supplier=self.suppliers[0], price=100), G(Product, supplier=self.suppliers[0], price=200)]
        products1 = [G(Product, supplier=self.suppliers[1], price=301)]
        self.restaurant = G(Restaurant)
        carts = [G(Cart, supplier=self.suppliers[0], product=products0[0], quantity=2, amount=200, restaurant=self.restaurant),
                 G(Cart, supplier=self.suppliers[0], product=products0[1], quantity=2, amount=400, restaurant=self.restaurant),
                 G(Cart, supplier=self.suppliers[1], product=products1[0], quantity=2, amount=602, restaurant=self.restaurant)]

    def test_send_orders(self):
        import ipdb
        ipdb.set_trace()
        json_request = {
            "data": [{
                "supplier": self.suppliers[0].id,
                "requested_delivery_date": "2019-12-27",
                "note": "A Tout le monde"
            },
                {
                    "supplier": self.suppliers[1].id,
                    "requested_delivery_date": "2020-12-27",
                    "note": "A Tout le monde2"
                }
            ],
            "restaurant_id": self.restaurant.id
        }
        url = "/orders/new/"
        response = self.call_post_api(url, json_request)

        # rather than check response, check the creation of order objects
        first_order = Order.objects.get(supplier=self.suppliers[0], restaurant=self.restaurant)
        self.assertEqual(first_order.amount, 600)
        self.assertEqual(first_order.comment, "A Tout le monde")

        second_order = Order.objects.get(supplier=self.suppliers[1], restaurant=self.restaurant)
        self.assertEqual(second_order.amount, 602)
        self.assertEqual(second_order.comment, "A Tout le monde2")

