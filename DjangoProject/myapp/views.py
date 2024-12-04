import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal


# Create your views here.
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, World!")


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')
            available = data.get('available')

            if not name or price is None or available is None:
                return HttpResponseBadRequest("Missing required fields: 'name', 'price', or 'available'.")

            try:
                price = Decimal(str(price))
            except (ValueError, TypeError):
                return HttpResponseBadRequest("'price' must be a valid number.")

            if not isinstance(available, bool):
                return HttpResponseBadRequest("'available' must be a boolean.")

            product = Product(name=name, price=price, available=available)
            product.full_clean()
            product.save()

            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            }, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format in request body.")

    else:
        return HttpResponseBadRequest("Method not allowed for this endpoint.")


@csrf_exempt
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
            return HttpResponseNotFound(f"Product with ID {product_id} not found.")

    else:
        return HttpResponseBadRequest("Method not allowed for this endpoint.")




