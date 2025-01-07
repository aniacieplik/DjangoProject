from django.test import TestCase
from myapp.models import Product, Customer
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(
            name='Valid Product',
            price=9.99,
            available=True
        )
        self.assertEqual(temp_product.name, 'Valid Product')
        self.assertEqual(temp_product.price, 9.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        product = Product(
            name='Invalid Product',
            price=-5.00,
            available=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_missing_price(self):
        product = Product(
            name='No Price Product',
            available=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_missing_name(self):
        product = Product(
            price=9.99,
            available=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_missing_available(self):
        product = Product(
            name='No Availability Product',
            price=9.99
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_too_short_name(self):
        product = Product(
            name='',
            price=9.99,
            available=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_too_long_name(self):
        long_name = 'P' * 256
        product = Product(
            name=long_name,
            price=9.99,
            available=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_min_price(self):
        temp_product = Product.objects.create(
            name='Min Price Product',
            price=0.01,
            available=True
        )
        self.assertEqual(temp_product.price, 0.01)

    def test_create_product_with_max_price(self):
        max_price = 99999.99
        temp_product = Product.objects.create(
            name='Max Price Product',
            price=max_price,
            available=True
        )
        self.assertEqual(temp_product.price, max_price)

    def test_create_product_with_invalid_price_format(self):
        product = Product(
            name='Invalid Price Format',
            price=9.999,
            available=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()



class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(
            name='John Doe',
            address='123 Main Street'
        )
        self.assertEqual(customer.name, 'John Doe')
        self.assertEqual(customer.address, '123 Main Street')

    def test_create_customer_with_missing_name(self):
        customer = Customer(
            address='123 Main Street'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_missing_address(self):
        customer = Customer(
            name='John Doe'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_blank_name(self):
        customer = Customer(
            name='',
            address='123 Main Street'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_blank_address(self):
        customer = Customer(
            name='John Doe',
            address=''
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_too_short_name(self):
        customer = Customer(
            name='',
            address='123 Main Street'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_too_long_name(self):
        long_name = 'A' * 256
        customer = Customer(
            name=long_name,
            address='123 Main Street'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_too_long_address(self):
        long_address = 'A' * 256

        customer = Customer(
            name='John Doe',
            address=long_address
        )

        with self.assertRaises(ValidationError) as context:
            customer.full_clean()

        self.assertIn('address', context.exception.message_dict)