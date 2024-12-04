import json
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Customer, Order
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.body = None
        self.data = None
        self.method = None

    @api_view(['GET'])
    def customer_list(self):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    def customer_detail(request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)


    @api_view(['GET'])
    def order_list(request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    @api_view(['POST'])
    def create_order(request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    @csrf_exempt
    def customer_detail(request, customer_id):
        if request.method == 'GET':
            try:
                customer = Customer.objects.get(id=customer_id)
                return JsonResponse({
                    'id': customer.id,
                    'name': customer.name,
                    'address': customer.address
                })
            except Customer.DoesNotExist:
                return JsonResponse({'error': 'Customer not found'}, status=404)


    @csrf_exempt
    def create_customer(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            name = data.get('name')
            address = data.get('address')
            if not name or not address:
                return JsonResponse({'error': 'Name and address are required'}, status=400)
            customer = Customer(name=name, address=address)
            customer.full_clean()
            customer.save()
            return JsonResponse({
                'id': customer.id,
                'name': customer.name,
                'address': customer.address
            }, status=201)

def customer_list(request):
    if request.method == 'GET':
        customers = list(Customer.objects.values('id', 'name', 'address'))
        return JsonResponse(customers, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        address = data.get('address')
        customer = Customer(name=name, address=address)
        customer.full_clean()
        customer.save()
        return JsonResponse({
           'id': customer.id,
           'name': customer.name,
           'address': customer.address
        }, status=201)

def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        price = data.get('price')
        available = data.get('available')
        product = Product(name=name, price=Decimal(str(price)), available=available)
        product.full_clean()
        product.save()
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        }, status=201)


def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            })
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)


def customer_detail(request, order_id):
    if request.method == 'GET':
        try:
            order = Order.objects.get(id=order_id)
            return JsonResponse({
                'id': order.id,
                'status': order.status,
                'customer': order.customer.id
            })
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)


def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


def order_list(request):
    if request.method == 'GET':
        orders = list(Order.objects.values('id', 'status', 'customer'))
        return JsonResponse(orders, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        status = data.get('status')
        customer = Customer.objects.get(id=customer_id)
        order = Order(customer=customer, status=status)
        order.save()
        return JsonResponse({
            'id': order.id,
            'status': order.status,
            'customer': order.customer.id
        }, status=201)


def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        status = data.get('status')
        customer = Customer.objects.get(id=customer_id)
        order = Order(customer=customer, status=status)
        order.save()
        return JsonResponse({
            'id': order.id,
            'status': order.status,
            'customer': order.customer.id
        }, status=201)