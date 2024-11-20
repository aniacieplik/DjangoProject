from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        for order in Order.objects.all():
            order.products.clear()

        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Sample Product 1',
            price=19.99,
            available=True
        )

        product2 = Product.objects.create(
            name='Sample Product 2',
            price=49.99,
            available=False
        )

        customer1 = Customer.objects.create(
            name='John Doe',
            address='123 Main Street, Anytown, USA'
        )

        customer2 = Customer.objects.create(
            name='Jane Smith',
            address='456 Elm Street, Othertown, USA'
        )

        order1 = Order.objects.create(
            customer=customer1,
            status='New'
        )
        order2 = Order.objects.create(
            customer=customer2,
            status='Completed'
        )

        order1.products.add(product1)
        order2.products.add(product2)

        self.stdout.write("Sample data created successfully.")