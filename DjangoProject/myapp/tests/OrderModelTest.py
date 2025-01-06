from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='John Doe',
            address='123 Main St'
        )
        self.product1 = Product.objects.create(
            name='Product 1',
            price=10.00,
            available=True
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            price=20.00,
            available=True
        )

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.customer.name, 'John Doe')
        self.assertEqual(order.status, 'New')
        self.assertEqual(order.products.count(), 2)

    def test_create_order_with_missing_customer(self):
        order = Order(
            status='New'
        )
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_create_order_with_invalid_status(self):
        order = Order(
            customer=self.customer,
            status='InvalidStatus'
        )
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_total_price_with_valid_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        total_price = sum(product.price for product in order.products.all())
        self.assertEqual(total_price, 30.00)

    def test_total_price_with_no_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        total_price = sum(product.price for product in order.products.all())
        self.assertEqual(total_price, 0.00)

    def test_order_fulfillment_with_available_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        can_fulfill = all(product.available for product in order.products.all())
        self.assertTrue(can_fulfill)

    def test_order_fulfillment_with_unavailable_products(self):
        self.product1.available = False
        self.product1.save()

        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        can_fulfill = all(product.available for product in order.products.all())
        self.assertFalse(can_fulfill)