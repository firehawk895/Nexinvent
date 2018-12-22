from django_dynamic_fixture import G
from rest_framework.test import APITestCase

from utility.generics_for_tests import TestCaseMixin


class SendAllOrders(APITestCase, TestCaseMixin):
    def setUp(self):
        pass

    def send_all_orders(self):
        request = {
            "data": [{
                "reqDD": None,
                "comment": "",
                "supplier": "1",
                "order_items": [{
                    "product": "1",
                    "quantity": 3,
                    "price": 788
                }]
            }, {
                "delivery_charge": 0,
                "reqDD": None,
                "comment": "",
                "supplier": "1",
                "order_items": [{
                    "product": "1",
                    "quantity": 1,
                    "price": 98
                }, {
                    "product": "1",
                    "quantity": 1,
                    "price": 165
                }]
            }]
        }