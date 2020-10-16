from django.test import TestCase
from .models import Order, OrderLineItem
from products.models import Product


class OrderModelTests(TestCase):

    def test_order_string_representation(self):
        """ test string representation of order profile """
        order = Order.objects.create(
            full_name='Hans Jansen',
        )
        self.assertEqual(str(order), order.order_reference)

    def test_orderlineitem_string_representation(self):
        """ test string representation of order line item """
        order = Order.objects.create(
            full_name='Hans Jansen',
        )
        product = Product.objects.create(
            name='Test Product',
            price=9.99
        )
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            lineitem_price_per_unit=9.99,
            lineitem_total=19.98,
        )
        self.assertEqual(str(order_line_item), 'Test Product (x2)')
