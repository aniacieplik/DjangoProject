from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/', include(router.urls)),
    path('product_list/', views.product_list, name='product_list'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer_detail/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create_order/', views.create_order, name='create_order'),
]
