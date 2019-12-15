from django.conf import settings
from mvp.models import Order

from mvp.tasks import send_whatsapp


def send_whatsapp_notifications(order):
    """
    Logic flow depends on the fact that we can determine the order placer and the order placee based on order status
    :return:
    """
    vendor_order_url = settings.FRONT_END_BASE_URL + "vendors/orders/" + str(order.id)
    if order.status == Order.SUBMITTED:
        # New order got created by the restaurant
        # -- Restaurant notification
        send_order_created_restaurant_notification(order.id, order.amount, order.supplier.name,
                                                   order.requested_delivery_date, order.restaurant.phone_number)
        # -- Supplier notification
        send_order_created_supplier_notification(order.id, order.amount, order.restaurant.name,
                                                 order.requested_delivery_date, order.supplier.phone_number)
    elif order.status == Order.ACCEPTED or order.status == Order.REJECTED:
        # Supplier accepted or rejected the order
        # -- Restaurant notification
        send_order_updatee_notification(order.id, order.amount, order.status, order.supplier.name, None,
                                        order.restaurant.phone_number)
        # -- Supplier notification
        send_order_updater_notification(order.status, order.id, order.amount,
                                        order.restaurant.name, vendor_order_url, order.supplier.phone_number)
    elif order.status == Order.CHECKED_IN:
        # Restaurant checked in the order
        # -- Restaurant notification
        send_order_updater_notification(order.status, order.id, order.amount_checked_in, order.supplier.name, None,
                                        order.restaurant.phone_number)
        # -- Supplier notification
        send_order_updatee_notification(order.id, order.amount_checked_in, order.status,
                                        order.restaurant.name, vendor_order_url, order.supplier.phone_number)
    elif order.status == Order.DELIVERED:
        # Restaurant marked the order as finalized
        # -- Restaurant notification
        status = "finalized"
        send_order_updater_notification(status, order.id, order.amount_checked_in, order.supplier.name, None,
                                        order.restaurant.phone_number)
        # -- Supplier notification
        status_supplier = "marked delivered"
        send_order_updatee_notification(order.id, order.amount_checked_in, status_supplier, order.restaurant.name, vendor_order_url,
                                        order.supplier.phone_number)


def send_order_created_restaurant_notification(order_id, amount, supplier_name, delivery_date, send_to_number):
    """
    Represents the whats app template:
    template_5:
    New order #{{1}} of amount ₹{{2}} has been placed with {{3}}. Delivery scheduled on {{4}}. \nDetails: {{5}}
    :param order_id:
    :param amount:
    :param supplier_name:
    :param delivery_date:
    :param send_to_number:
    :return:
    """
    order_id = "*" + str(order_id) + "*"
    amount = "*" + str(round(amount, 2)) + "*"
    supplier_name = "*" + supplier_name + "*"
    delivery_date = "*" + str(delivery_date) + "*"
    message = "New order #{} of amount ₹{} has been placed with {}. Delivery scheduled on {}. \nDetails: {}".format(
        order_id, amount, supplier_name, delivery_date, None)
    send_whatsapp(send_to_number, message)


def send_order_created_supplier_notification(order_id, amount, restaurant_name, delivery_date, send_to_number):
    """
    Represents the whats app template:
    template_2:
    New order received from {{1}}, order #{{2}}, Amount: ₹ {{3}}. Requested Delivery date : {{4}}. \nTo Accept/Reject click {{5}}
    :param order_id:
    :param amount:
    :param restaurant_name:
    :param delivery_date:
    :param send_to_number:
    :return:
    """
    url = settings.FRONT_END_BASE_URL + "vendors/orders/" + str(order_id)
    order_id = "*" + str(order_id) + "*"
    amount = "*" + str(round(amount, 2)) + "*"
    restaurant_name = "*" + restaurant_name + "*"
    delivery_date = "*" + str(delivery_date) + "*"

    message = "New order received from {}, order #{}, Amount: ₹ {}. Requested Delivery date : {}. \nTo Accept/Reject click {}".format(
        restaurant_name, order_id, amount,
        delivery_date, url)
    send_whatsapp(send_to_number, message)


def send_order_updater_notification(action, order_id, amount, updatee_name, url, send_to_number):
    """
    Represents the whats app template:
    template_4:
    Order Update: You have {{1}} order {{2}} of Amount ₹{{3}} for {{4}}. \nDetails: {{5}}
    :param action:
    :param order_id:
    :param amount:
    :param updatee_name:
    :param url:
    :param send_to_number:
    :return:
    """
    order_id = "*#" + str(order_id) + "*"
    amount = "*" + str(round(amount, 2)) + "*"
    action = "*" + action + "*"
    updatee_name = "*" + updatee_name + "*"
    message = "Order Update: You have {} order {} of Amount ₹{} for {}. \nDetails: {}".format(action, order_id, amount, updatee_name, url)
    send_whatsapp(send_to_number, message)


def send_order_updatee_notification(order_id, amount, action, updater_name, url, send_to_number):
    """
    Represents the whats app template:
    template_3:
    Order Update: Order #{{1}} of Amount ₹{{2}} has been {{3}} by {{4}}. \nOrder Details: {{5}}
    :param order_id:
    :param amount:
    :param action:
    :param updater_name:
    :param url:
    :param send_to_number:
    :return:
    """
    order_id = "*" + str(order_id) + "*"
    amount = "*" + str(round(amount, 2)) + "*"
    action = "*" + action + "*"
    updater_name = "*" + updater_name + "*"
    message = "Order Update: Order #{} of Amount ₹{} has been {} by {}. \nOrder Details: {}".format(order_id, amount, action, updater_name, url)
    send_whatsapp(send_to_number, message)