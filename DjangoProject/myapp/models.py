from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0)
    ])
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed')
    ])
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Order {self.id} - {self.status}"