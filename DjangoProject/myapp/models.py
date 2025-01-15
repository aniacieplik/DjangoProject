from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("In Process", "In Process"),
        ("Sent", "Sent"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.id} for {self.customer}"

    def total_price(self):
        return sum(product.price for product in self.products.all())

    def if_can_be_fulfilled(self):
        return all(product.available for product in self.products.all())